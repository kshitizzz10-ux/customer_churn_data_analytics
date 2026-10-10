"""
scripts/generate_presentation.py
Generates a polished, professional 3-slide executive presentation in PowerPoint format
following Big 4 / PwC consulting standards:
- Slide 1: The Problem (Context, Churn Rate, Financial Bleed)
- Slide 2: The Findings (Three Root Causes Accounting for 80% of Churn)
- Slide 3: The Recommendations (Three Strategies to Save $520K+ in ARR with ROI)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_PPTX = os.path.join("deliverables", "Executive_Summary.pptx")
os.makedirs(os.path.dirname(OUTPUT_PPTX), exist_ok=True)

# Colors
C_DARK_NAVY = RGBColor(30, 41, 59)      # #1E293B
C_PWC_ORANGE = RGBColor(208, 74, 2)     # #D04A02
C_SLATE_GRAY = RGBColor(100, 116, 139)  # #64748B
C_LIGHT_BG = RGBColor(248, 250, 252)    # #F8FAFC
C_WHITE = RGBColor(255, 255, 255)
C_CARD_BORDER = RGBColor(226, 232, 240) # #E2E8F0
C_GREEN = RGBColor(22, 163, 74)         # #16A34A
C_AMBER = RGBColor(217, 119, 6)         # #D97706

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def add_header(slide, title_text, category_text):
    # Top banner line
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_PWC_ORANGE
    top_bar.line.fill.background()

    # Category / Tracker
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = C_PWC_ORANGE

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.8))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = C_DARK_NAVY

def add_footer(slide, current_page):
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.4))
    tf = footer_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"PwC Technology Consulting Practice | TelcoMax Retention Strategy Engagement • Page {current_page} of 3"
    p.font.size = Pt(10)
    p.font.color.rgb = C_SLATE_GRAY

# ==============================================================================
# SLIDE 1: THE BUSINESS PROBLEM
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
add_header(s1, "TelcoMax Is Losing $1.67M Annually in Recurring Revenue to Customer Churn", "Client Executive Brief & Problem Definition")

# Left Column: Strategic Narrative
narrative_bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(6.8), Inches(4.8))
narrative_bg.fill.solid()
narrative_bg.fill.fore_color.rgb = C_WHITE
narrative_bg.line.color.rgb = C_CARD_BORDER

tf1 = narrative_bg.text_frame
tf1.word_wrap = True
tf1.margin_left = Inches(0.3)
tf1.margin_right = Inches(0.3)
tf1.margin_top = Inches(0.3)

p = tf1.paragraphs[0]
p.text = "Executive Engagement Context & Baseline Diagnostics:"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = C_DARK_NAVY
p.space_after = Pt(12)

points = [
    ("Critical Subscriber Bleed: ", "TelcoMax is experiencing an annualized customer churn rate of 26.54%, driven by heavy month-over-month attrition among high-value subscribers."),
    ("Severe Financial Bleed: ", "Historical churn directly removes $139,131/month in recurring cash flow ($1,669,570 in annualized ARR). Furthermore, forward predictive scoring identifies an additional $406,543 in active ARR currently sitting in the High-Risk tier."),
    ("Client Mandate & Scope: ", "PwC was engaged to conduct end-to-end root cause diagnostics across 7,043 subscriber records, build proactive machine learning risk scoring, and formulate prioritized commercial retention strategies to stop the bleed."),
    ("Core Consulting Deliverable: ", "Transition TelcoMax from reactive reporting to an automated, predictive retention engine that arms account managers with targeted subscriber intervention lists.")
]

for title_pt, body_pt in points:
    p = tf1.add_paragraph()
    p.space_after = Pt(10)
    run_t = p.add_run()
    run_t.text = "• " + title_pt
    run_t.font.bold = True
    run_t.font.size = Pt(12)
    run_t.font.color.rgb = C_DARK_NAVY
    
    run_b = p.add_run()
    run_b.text = body_pt
    run_b.font.size = Pt(12)
    run_b.font.color.rgb = C_SLATE_GRAY

# Right Column: Big KPI Stat Cards
kpi_card1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.0), Inches(1.8), Inches(4.5), Inches(2.25))
kpi_card1.fill.solid()
kpi_card1.fill.fore_color.rgb = C_WHITE
kpi_card1.line.color.rgb = C_PWC_ORANGE
kpi_card1.line.width = Pt(2)

tf_k1 = kpi_card1.text_frame
tf_k1.margin_left = Inches(0.3)
tf_k1.margin_top = Inches(0.25)
p = tf_k1.paragraphs[0]
p.text = "ANNUAL REVENUE AT RISK (HISTORICAL CHURN)"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_SLATE_GRAY

p2 = tf_k1.add_paragraph()
p2.text = "$1,669,570"
p2.font.size = Pt(36)
p2.font.bold = True
p2.font.color.rgb = C_PWC_ORANGE

p3 = tf_k1.add_paragraph()
p3.text = "1,869 churned accounts • $139.1K / month cash drain"
p3.font.size = Pt(11)
p3.font.color.rgb = C_SLATE_GRAY

kpi_card2 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.0), Inches(4.35), Inches(4.5), Inches(2.25))
kpi_card2.fill.solid()
kpi_card2.fill.fore_color.rgb = C_WHITE
kpi_card2.line.color.rgb = C_CARD_BORDER

tf_k2 = kpi_card2.text_frame
tf_k2.margin_left = Inches(0.3)
tf_k2.margin_top = Inches(0.25)
p = tf_k2.paragraphs[0]
p.text = "ACTIVE HIGH-RISK ARR (FORWARD EXPOSURE)"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_SLATE_GRAY

p2 = tf_k2.add_paragraph()
p2.text = "$406,543"
p2.font.size = Pt(36)
p2.font.bold = True
p2.font.color.rgb = C_DARK_NAVY

p3 = tf_k2.add_paragraph()
p3.text = "434 active accounts with ≥ 70% model churn probability"
p3.font.size = Pt(11)
p3.font.color.rgb = C_SLATE_GRAY

add_footer(s1, 1)

# ==============================================================================
# SLIDE 2: THE ROOT CAUSES (FINDINGS)
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "Three Structural Root Causes Account for Over 80% of Customer Churn", "Diagnostic Findings & Machine Learning Insights")

col_width = Inches(3.7)
col_gap = Inches(0.3)
left_margin = Inches(0.8)

columns_data = [
    {
        "num": "01",
        "title": "Contract Structure",
        "subtitle": "Month-to-Month Exposure",
        "stat": "42.7%",
        "stat_label": "Month-to-Month Churn Rate",
        "color": C_PWC_ORANGE,
        "bullets": [
            "Month-to-month subscribers churn at 42.7% vs. only 2.8% on two-year agreements.",
            "Represents 88.5% (1,655 accounts) of all churned subscribers.",
            "Drives $1,450,165 in annual lost ARR.",
            "Insight: Absence of contractual switching barriers leaves customers vulnerable to competitor promotional churn."
        ]
    },
    {
        "num": "02",
        "title": "Onboarding Cliff",
        "subtitle": "0 - 12 Month Vulnerability",
        "stat": "47.4%",
        "stat_label": "First-Year Cohort Churn Rate",
        "color": C_DARK_NAVY,
        "bullets": [
            "Nearly half of all new subscribers churn within the first 12 months.",
            "Represents 55.5% (1,037 accounts) of total company attrition.",
            "Sharpest attrition drop occurs between Month 1 and Month 6.",
            "Insight: Points directly to friction in first-time user experience, customer onboarding gaps, and early invoice sticker shock."
        ]
    },
    {
        "num": "03",
        "title": "Service Gaps & Friction",
        "subtitle": "Fiber & Payment Friction",
        "stat": "45.3%",
        "stat_label": "Electronic Check Churn Rate",
        "color": C_AMBER,
        "bullets": [
            "Fiber optic customers churn at 41.9% (vs 19.0% DSL) despite premium ARPU ($91/mo).",
            "Electronic check payments exhibit 45.3% churn vs 15.2% for auto-credit cards.",
            "Subscribers with 5+ add-ons churn at <13% vs 45.8% for 1 add-on.",
            "Insight: Service depth dramatically increases stickiness; manual payment methods introduce monthly cancellation reconsiderations."
        ]
    }
]

for i, col in enumerate(columns_data):
    x_pos = left_margin + i * (col_width + col_gap)
    card = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, x_pos, Inches(1.8), col_width, Inches(4.8))
    card.fill.solid()
    card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = C_CARD_BORDER
    card.line.width = Pt(1.5)

    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)

    # Number + Category
    p = tf.paragraphs[0]
    p.text = f"PILLAR {col['num']} • {col['title'].upper()}"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = col["color"]
    p.space_after = Pt(4)

    # Subtitle
    p_sub = tf.add_paragraph()
    p_sub.text = col["subtitle"]
    p_sub.font.size = Pt(15)
    p_sub.font.bold = True
    p_sub.font.color.rgb = C_DARK_NAVY
    p_sub.space_after = Pt(8)

    # Big Metric
    p_stat = tf.add_paragraph()
    p_stat.text = col["stat"]
    p_stat.font.size = Pt(32)
    p_stat.font.bold = True
    p_stat.font.color.rgb = col["color"]
    p_stat.space_after = Pt(2)

    p_sl = tf.add_paragraph()
    p_sl.text = col["stat_label"]
    p_sl.font.size = Pt(10)
    p_sl.font.color.rgb = C_SLATE_GRAY
    p_sl.space_after = Pt(14)

    # Bullets
    for b in col["bullets"]:
        p_b = tf.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = C_DARK_NAVY
        p_b.space_after = Pt(6)

add_footer(s2, 2)

# ==============================================================================
# SLIDE 3: STRATEGIC RECOMMENDATIONS & FINANCIAL IMPACT
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "Three Targeted Commercial Strategies to Retain $520,000+ in Annual Recurring Revenue", "Strategic Retention Roadmap & Business Case")

# Top 3 Recommendations Cards
recs = [
    {
        "rec_num": "STRATEGY 1",
        "title": "'Lock-In' Contract Migration",
        "desc": "Offer a targeted 10–12% promotional discount or complementary streaming bundle for high-risk month-to-month customers who commit to a 12-month contract.",
        "target": "Target: 1,500 High-Risk MTM Accounts",
        "savings": "+$240K / Year",
        "color": C_PWC_ORANGE
    },
    {
        "rec_num": "STRATEGY 2",
        "title": "90-Day Proactive Onboarding",
        "desc": "Implement automated Day 7, 30, 60, and 90 customer success check-ins, accompanied by dedicated white-glove tech setup for new fiber optic subscribers.",
        "target": "Target: 2,100 New Subscribers (<12m)",
        "savings": "+$165K / Year",
        "color": C_DARK_NAVY
    },
    {
        "rec_num": "STRATEGY 3",
        "title": "Security Bundle & Auto-Pay Push",
        "desc": "Cross-sell a discounted 'Digital Protection Bundle' (TechSupport + OnlineSecurity) paired with a $5/month discount for switching from Electronic Check to Auto-Pay.",
        "target": "Target: 1,200 Single-Service Accounts",
        "savings": "+$115K / Year",
        "color": C_GREEN
    }
]

rec_width = Inches(3.7)
for i, rec in enumerate(recs):
    x_pos = left_margin + i * (rec_width + col_gap)
    card = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, x_pos, Inches(1.8), rec_width, Inches(3.2))
    card.fill.solid()
    card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = C_CARD_BORDER

    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.2)

    p = tf.paragraphs[0]
    p.text = rec["rec_num"]
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = rec["color"]
    p.space_after = Pt(2)

    p2 = tf.add_paragraph()
    p2.text = rec["title"]
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK_NAVY
    p2.space_after = Pt(6)

    p3 = tf.add_paragraph()
    p3.text = rec["desc"]
    p3.font.size = Pt(11)
    p3.font.color.rgb = C_SLATE_GRAY
    p3.space_after = Pt(10)

    p4 = tf.add_paragraph()
    p4.text = rec["target"]
    p4.font.size = Pt(10)
    p4.font.bold = True
    p4.font.color.rgb = C_DARK_NAVY
    p4.space_after = Pt(4)

    p5 = tf.add_paragraph()
    p5.text = f"Retained ARR: {rec['savings']}"
    p5.font.size = Pt(13)
    p5.font.bold = True
    p5.font.color.rgb = rec["color"]

# Bottom Summary Banner: ROI & Next Steps
summary_card = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.4))
summary_card.fill.solid()
summary_card.fill.fore_color.rgb = C_DARK_NAVY
summary_card.line.fill.background()

tf_sum = summary_card.text_frame
tf_sum.word_wrap = True
tf_sum.margin_left = Inches(0.35)
tf_sum.margin_top = Inches(0.2)

p_sum1 = tf_sum.paragraphs[0]
p_sum1.text = "BUSINESS CASE SUMMARY & NEXT STEPS (Q1 IMPLEMENTATION)"
p_sum1.font.size = Pt(11)
p_sum1.font.bold = True
p_sum1.font.color.rgb = C_PWC_ORANGE
p_sum1.space_after = Pt(4)

p_sum2 = tf_sum.add_paragraph()
p_sum2.text = "• Quantified Impact: Combined retention initiatives project $520,000+ in annual retained recurring revenue (~31% reduction in total ARR loss) against an estimated campaign execution budget of $110,000 (Projected ROI: ~4.7x).\n• Recommended Next Step: Launch a 90-day pilot for Strategy 1 targeting the top 400 highest-value active accounts flagged in the model scoring output. Monitor conversion and retention lift before general portfolio rollout."
p_sum2.font.size = Pt(11)
p_sum2.font.color.rgb = C_WHITE

add_footer(s3, 3)

prs.save(OUTPUT_PPTX)
print(f"[+] Consulting presentation successfully saved to: {OUTPUT_PPTX}")
