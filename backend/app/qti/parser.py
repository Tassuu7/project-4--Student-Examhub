"""
ExamHub QTI (Question and Test Interoperability) Parser
Parses IMS Global QTI 2.1 / 3.0 assessment items from XML documents into ExamHub models.
"""

import xml.etree.ElementTree as ET
from typing import List, Optional, Tuple
from backend.app.qti.schemas import (
    QTIAssessmentItem,
    QTIInteractionType,
    QTIResponseDeclaration,
    QTISimpleChoice,
    QTIModalFeedback,
    QTIImportResult,
)


class QTIParser:
    """
    Parser for IMS Global QTI AssessmentItem XML format.
    Tolerates various namespace conventions (qti, default xml namespace).
    """

    @classmethod
    def _strip_ns(cls, tag: str) -> str:
        """Removes XML namespace prefix if present: {http://...}tag -> tag"""
        if "}" in tag:
            return tag.split("}", 1)[1]
        return tag

    @classmethod
    def parse_assessment_item_xml(cls, xml_text: str) -> Optional[QTIAssessmentItem]:
        """
        Parses a single QTI 2.1 assessmentItem XML string.
        """
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as e:
            return None

        # Clean tags
        root_tag = cls._strip_ns(root.tag)
        if root_tag != "assessmentItem":
            return None

        identifier = root.attrib.get("identifier", "unknown_item")
        title = root.attrib.get("title", identifier)
        adaptive = root.attrib.get("adaptive", "false").lower() == "true"
        time_dependent = root.attrib.get("timeDependent", "false").lower() == "true"

        # Find responseDeclaration
        response_decl = None
        for child in root:
            if cls._strip_ns(child.tag) == "responseDeclaration":
                r_id = child.attrib.get("identifier", "RESPONSE")
                cardinality = child.attrib.get("cardinality", "single")
                base_type = child.attrib.get("baseType", "identifier")
                correct_resps = []

                for sub in child:
                    if cls._strip_ns(sub.tag) == "correctResponse":
                        for val in sub:
                            if cls._strip_ns(val.tag) == "value" and val.text:
                                correct_resps.append(val.text.strip())

                response_decl = QTIResponseDeclaration(
                    identifier=r_id,
                    cardinality=cardinality,
                    base_type=base_type,
                    correct_response=correct_resps
                )
                break

        if not response_decl:
            response_decl = QTIResponseDeclaration(identifier="RESPONSE")

        # Find itemBody
        prompt_text = ""
        interaction_type = QTIInteractionType.CHOICE
        choices: List[QTISimpleChoice] = []

        for child in root:
            if cls._strip_ns(child.tag) == "itemBody":
                for elem in child:
                    tag_name = cls._strip_ns(elem.tag)
                    if tag_name == "p" and not prompt_text:
                        prompt_text = "".join(elem.itertext()).strip()
                    elif tag_name == "choiceInteraction":
                        interaction_type = QTIInteractionType.CHOICE
                        for opt in elem:
                            opt_tag = cls._strip_ns(opt.tag)
                            if opt_tag == "prompt" and not prompt_text:
                                prompt_text = "".join(opt.itertext()).strip()
                            elif opt_tag == "simpleChoice":
                                opt_id = opt.attrib.get("identifier", "")
                                opt_fixed = opt.attrib.get("fixed", "false").lower() == "true"
                                opt_content = "".join(opt.itertext()).strip()
                                choices.append(
                                    QTISimpleChoice(
                                        identifier=opt_id,
                                        fixed=opt_fixed,
                                        content=opt_content
                                    )
                                )
                    elif tag_name == "extendedTextInteraction":
                        interaction_type = QTIInteractionType.EXTENDED_TEXT
                        for opt in elem:
                            if cls._strip_ns(opt.tag) == "prompt" and not prompt_text:
                                prompt_text = "".join(opt.itertext()).strip()
                    elif tag_name == "textEntryInteraction":
                        interaction_type = QTIInteractionType.TEXT_ENTRY

        # Find modalFeedback
        feedbacks: List[QTIModalFeedback] = []
        for child in root:
            if cls._strip_ns(child.tag) == "modalFeedback":
                fb_id = child.attrib.get("identifier", "fb")
                outcome = child.attrib.get("outcomeIdentifier", "FEEDBACK")
                show_hide = child.attrib.get("showHide", "show")
                title = child.attrib.get("title", "")
                content = "".join(child.itertext()).strip()
                feedbacks.append(
                    QTIModalFeedback(
                        identifier=fb_id,
                        outcome_identifier=outcome,
                        show_hide=show_hide,
                        title=title,
                        content=content
                    )
                )

        return QTIAssessmentItem(
            identifier=identifier,
            title=title,
            adaptive=adaptive,
            time_dependent=time_dependent,
            interaction_type=interaction_type,
            prompt=prompt_text or "No prompt provided",
            choices=choices,
            response_declaration=response_decl,
            feedback=feedbacks,
            max_score=1.0
        )

    @classmethod
    def parse_package_zip_entries(cls, file_data_map: dict) -> QTIImportResult:
        """
        Parses a collection of XML files extracted from an uploaded QTI zip bundle.
        """
        imported_ids = []
        warnings = []
        failed = 0

        for filename, content in file_data_map.items():
            if not filename.endswith(".xml") or filename.endswith("manifest.xml"):
                continue

            try:
                xml_str = content.decode("utf-8") if isinstance(content, bytes) else str(content)
                item = cls.parse_assessment_item_xml(xml_str)
                if item:
                    imported_ids.append(item.identifier)
                else:
                    failed += 1
                    warnings.append(f"Failed to parse valid assessmentItem from {filename}")
            except Exception as e:
                failed += 1
                warnings.append(f"Error reading {filename}: {str(e)}")

        return QTIImportResult(
            imported_count=len(imported_ids),
            failed_count=failed,
            items_imported=imported_ids,
            validation_warnings=warnings
        )
