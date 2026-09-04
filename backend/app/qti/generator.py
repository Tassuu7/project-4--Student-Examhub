"""
ExamHub QTI (Question and Test Interoperability) Generator
Generates standards-compliant IMS QTI 2.1 XML items and imsmanifest.xml documents.
"""

import xml.sax.saxutils as saxutils
from typing import List, Optional
from datetime import datetime, timezone
from backend.app.qti.schemas import (
    QTIAssessmentItem,
    QTIPackageExportResponse,
    QTIInteractionType,
)


class QTIGenerator:
    """
    Serializes ExamHub question objects into valid IMS QTI 2.1 XML.
    """

    @classmethod
    def generate_assessment_item_xml(cls, item: QTIAssessmentItem) -> str:
        """
        Produce valid QTI 2.1 XML string for an assessment item.
        """
        prompt_escaped = saxutils.escape(item.prompt)
        title_escaped = saxutils.escape(item.title)

        correct_values = "".join(
            f"<value>{saxutils.escape(val)}</value>"
            for val in item.response_declaration.correct_response
        )

        choices_xml = ""
        for choice in item.choices:
            choice_content = saxutils.escape(choice.content)
            choices_xml += f"""
        <simpleChoice identifier="{choice.identifier}" fixed="{'true' if choice.fixed else 'false'}">
            {choice_content}
        </simpleChoice>"""

        feedback_xml = ""
        for fb in item.feedback:
            feedback_xml += f"""
    <modalFeedback outcomeIdentifier="{fb.outcome_identifier}" identifier="{fb.identifier}" showHide="{fb.show_hide}" title="{saxutils.escape(fb.title)}">
        <p>{saxutils.escape(fb.content)}</p>
    </modalFeedback>"""

        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<assessmentItem xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqti_v2p1 http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1.xsd"
                identifier="{item.identifier}"
                title="{title_escaped}"
                adaptive="{'true' if item.adaptive else 'false'}"
                timeDependent="{'true' if item.time_dependent else 'false'}">

    <responseDeclaration identifier="{item.response_declaration.identifier}"
                         cardinality="{item.response_declaration.cardinality}"
                         baseType="{item.response_declaration.base_type}">
        <correctResponse>
            {correct_values}
        </correctResponse>
    </responseDeclaration>

    <outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float">
        <defaultValue>
            <value>0</value>
        </defaultValue>
    </outcomeDeclaration>

    <itemBody>
        <p>{prompt_escaped}</p>
        <choiceInteraction responseIdentifier="{item.response_declaration.identifier}" shuffle="true" maxChoices="1">{choices_xml}
        </choiceInteraction>
    </itemBody>
{feedback_xml}
</assessmentItem>"""
        return xml.strip()

    @classmethod
    def generate_manifest_xml(cls, items: List[QTIAssessmentItem], package_title: str) -> str:
        """
        Generate imsmanifest.xml declaring all assessment items in the package.
        """
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        resources_xml = ""

        for item in items:
            filename = f"{item.identifier}.xml"
            resources_xml += f"""
        <resource identifier="res_{item.identifier}" type="imsqti_item_xmlv2p1" href="{filename}">
            <file href="{filename}"/>
        </resource>"""

        manifest = f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns="http://www.imsglobal.org/xsd/imscp_v1p1"
          xmlns:imsmd="http://www.imsglobal.org/xsd/imsmd_v1p2"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          identifier="MANIFEST-{now_str}"
          xsi:schemaLocation="http://www.imsglobal.org/xsd/imscp_v1p1 http://www.imsglobal.org/xsd/imscp_v1p1.xsd">
    <metadata>
        <schema>IMS Content</schema>
        <schemaversion>1.2</schemaversion>
        <imsmd:lom>
            <imsmd:general>
                <imsmd:title>
                    <imsmd:langstring xml:lang="en">{saxutils.escape(package_title)}</imsmd:langstring>
                </imsmd:title>
            </imsmd:general>
        </imsmd:lom>
    </metadata>
    <organizations default="DEFAULT_ORG"/>
    <resources>{resources_xml}
    </resources>
</manifest>"""
        return manifest.strip()
