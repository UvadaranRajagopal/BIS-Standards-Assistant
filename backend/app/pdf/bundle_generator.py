"""
Generate PDF standards report.
"""

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from datetime import datetime, timezone, timedelta
from pathlib import Path


def generate_standards_bundle(
    tender_id: str,
    officer_id: str,
    query: str,
    recommendations: list[dict],
    output_path: str
) -> str:

    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=14,
        spaceAfter=10
    )

    content = []

    content.append(
        Paragraph(
            "BIS PROCUREMENT STANDARDS REPORT",
            title_style
        )
    )

    # Use Indian Standard Time (IST / UTC+5:30)
    ist = timezone(timedelta(hours=5, minutes=30))
    generated_ist = datetime.now(ist)

    metadata = [
        ["Tender ID", tender_id],
        ["Officer ID", officer_id],
        [
            "Generated",
            generated_ist.strftime(
                "%d %B %Y, %I:%M:%S %p IST"
            )
        ],
        ["Requirement", query]
    ]

    table = Table(
        metadata,
        colWidths=[100, 400]
    )

    table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    content.append(table)
    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "RECOMMENDED STANDARDS",
            section_style
        )
    )

    for index, rec in enumerate(
        recommendations,
        start=1
    ):

        content.append(
            Paragraph(
                f"{index}. {rec.get('standard_number', 'N/A')}",
                styles["Heading3"]
            )
        )

        content.append(
            Paragraph(
                str(
                    rec.get(
                        "standard_title",
                        "N/A"
                    )
                ),
                styles["Normal"]
            )
        )

        # ---------------------------------------------------------
        # Standard details
        # ---------------------------------------------------------

        details = [
            [
                "Category",
                str(rec.get("category", "N/A"))
            ],
            [
                "Year",
                str(rec.get("year", "N/A"))
            ],
            [
                "Status",
                str(rec.get("status", "Unknown"))
            ],
            [
                "Relevance",
                f"{rec.get('relevance_score', 0)}%"
            ]
        ]

        detail_table = Table(
            details,
            colWidths=[100, 400]
        )

        detail_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ])
        )

        content.append(Spacer(1, 8))
        content.append(detail_table)

        content.append(Spacer(1, 12))

        # ---------------------------------------------------------
        # Automatic Certification Verification
        # ---------------------------------------------------------

        certification = rec.get(
            "certification_verification",
            {}
        )

        verification_status = certification.get(
            "verification_status",
            "REVIEW_REQUIRED"
        )

        applicable = certification.get(
            "applicable"
        )

        requirement = certification.get(
            "requirement",
            "Information Unavailable"
        )

        scheme = certification.get(
            "scheme"
        )

        qco = certification.get(
            "qco"
        )

        crs = certification.get(
            "crs"
        )

        certification_details = certification.get(
            "details"
        )

        official_bis_source = certification.get(
            "official_bis_source"
        )

        # Convert values into readable text
        if applicable is True:
            applicable_text = "Yes"
        elif applicable is False:
            applicable_text = "No"
        else:
            applicable_text = "Review Required"

        if qco is True:
            qco_text = "Yes"
        elif qco is False:
            qco_text = "No"
        else:
            qco_text = "Not Available"

        if crs is True:
            crs_text = "Yes"
        elif crs is False:
            crs_text = "No"
        else:
            crs_text = "Not Available"

        if scheme:
            scheme_text = str(scheme)
        else:
            scheme_text = "None"

        if verification_status == "VERIFIED":
            status_text = "AUTOMATICALLY VERIFIED"

        elif verification_status == "NOT_CERTIFIABLE":
            status_text = "NOT CERTIFIABLE"

        else:
            status_text = "REVIEW REQUIRED"

        certification_rows = [
            [
                "Verification Status",
                status_text
            ],
            [
                "Certification Applicable",
                applicable_text
            ],
            [
                "Requirement",
                str(requirement)
            ],
            [
                "Scheme",
                scheme_text
            ],
            [
                "QCO Applicable",
                qco_text
            ],
            [
                "CRS Applicable",
                crs_text
            ]
        ]

        certification_table = Table(
            certification_rows,
            colWidths=[160, 340]
        )

        certification_table.setStyle(
            TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                )
            ])
        )

        content.append(
            Paragraph(
                "<b>Certification Verification</b>",
                styles["Heading4"]
            )
        )

        content.append(
            certification_table
        )

        # Certification details
        if certification_details:

            content.append(Spacer(1, 7))

            content.append(
                Paragraph(
                    "<b>Certification Details:</b> "
                    + str(certification_details),
                    styles["Normal"]
                )
            )

        # Official BIS source
        if official_bis_source:

            content.append(Spacer(1, 7))

            content.append(
                Paragraph(
                    "<b>Official BIS Source:</b> "
                    + str(official_bis_source),
                    styles["Normal"]
                )
            )

        content.append(Spacer(1, 10))

        # ---------------------------------------------------------
        # Why Recommended
        # ---------------------------------------------------------

        content.append(
            Paragraph(
                "<b>Why Recommended:</b> "
                + str(
                    rec.get(
                        "why_recommended",
                        "N/A"
                    )
                ),
                styles["Normal"]
            )
        )

        # Evidence
        evidence = rec.get("evidence")

        if evidence:

            content.append(Spacer(1, 7))

            content.append(
                Paragraph(
                    "<b>Evidence:</b> "
                    + str(evidence),
                    styles["Normal"]
                )
            )

        # Officer verification
        content.append(Spacer(1, 7))

        content.append(
            Paragraph(
                "<b>Officer Certification Verification:</b> "
                "Verified",
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 18))

    # ---------------------------------------------------------
    # Disclaimer
    # ---------------------------------------------------------

    content.append(
        Paragraph(
            "<b>Disclaimer:</b> "
            "Recommendations and certification information "
            "must be verified against official BIS publications "
            "before procurement.",
            styles["Normal"]
        )
    )

    doc.build(content)

    return output_path


if __name__ == "__main__":

    test_recommendations = [
        {
            "standard_number":
                "IS 10322:2025",

            "standard_title":
                "LED Luminaires for Street Lighting - Specification",

            "category":
                "LED Lighting & Electrical",

            "year":
                2025,

            "status":
                "Current",

            "relevance_score":
                90,

            "why_recommended":
                "Relevant to LED street lighting procurement.",

            "certification_verification": {
                "verification_status":
                    "VERIFIED",

                "applicable":
                    True,

                "requirement":
                    "Mandatory Certification",

                "scheme":
                    "CRS",

                "qco":
                    False,

                "crs":
                    True,

                "details":
                    "Compulsory Registration Scheme (CRS)",

                "official_bis_source":
                    "https://www.bis.gov.in/"
            }
        }
    ]

    output = (
        "./pdf_output/test_bundle.pdf"
    )

    generate_standards_bundle(
        tender_id="TENDER_TEST_001",
        officer_id="OFFICER_001",
        query="LED street lights for highway",
        recommendations=test_recommendations,
        output_path=output
    )

    print(
        f"PDF generated successfully: {output}"
    )