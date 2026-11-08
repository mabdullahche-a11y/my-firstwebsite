"""Build the standalone clinic pages. Run with Python 3 from the workspace."""

from html import escape as e
from pathlib import Path
import re
from urllib.parse import quote

from treatment_guides import GUIDES

ROOT = Path(__file__).resolve().parent / "dist"
ASSETS = ROOT / "assets"
PHONE = "923215928003"
GOOGLE = "https://share.google/6XlMzvFDFLPShELVK"
MAP = "https://www.google.com/maps?cid=15583772744485051348"
INSTA = "https://www.instagram.com/theladydentist.guj/"
NHS = "https://www.nhs.uk/live-well/healthy-teeth-and-gums/dental-treatments/"


def whatsapp(topic=""):
    message = f"Hello, I’d like to ask about an appointment for {topic.lower()}." if topic else "Hello, I’d like to request a dental appointment."
    return f"https://wa.me/{PHONE}?text={quote(message)}"


def button(href, label):
    return f'<a class="button" href="{e(href)}">{e(label)} <span aria-hidden="true">→</span></a>'


def picture(name, alt, lazy=True):
    loading = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return f'<img src="assets/{e(name)}" alt="{e(alt)}"{loading}>'


def page(slug, title, description, content):
    html = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | The Lady Dentist</title><meta name="description" content="{e(description)}">
<meta name="theme-color" content="#fffaf7"><link rel="icon" href="assets/clinic-logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400..800&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap">
<link rel="stylesheet" href="style.css"><script defer src="page.js"></script><script defer src="site.js"></script>
</head><body>
<a class="skip" href="#main">Skip to content</a>
<div class="topline"><a href="contact.html">Main G.T. Road, Gujranwala</a><span></span><a href="tel:+{PHONE}">+92 321 5928003</a></div>
<header class="header"><div class="wrap nav site-nav">
<a class="brand" href="index.html">{picture("clinic-logo.jpg", "", False)}<span>The Lady Dentist<small>GUJRANWALA</small></span></a>
<nav aria-label="Main navigation"><a href="services.html">Treatments</a><a href="results.html">Results</a><a href="about.html">Our story</a><a href="blog.html">Blog</a><a href="contact.html">Visit</a></nav>
{button(whatsapp(), "Book on WhatsApp")}
</div></header>
<main id="main">{content}</main>
{footer()}
</body></html>"""
    (ROOT / f"{slug}.html").write_text(html, encoding="utf-8")


def footer():
    return f"""<footer class="site-footer"><div class="wrap footer-columns">
<div><a class="brand" href="index.html">{picture("clinic-logo.jpg", "", False)} The Lady Dentist</a><p>Dental care on Main G.T. Road, Gujranwala.</p></div>
<div><strong>Explore</strong><a href="services.html">Treatments</a><a href="results.html">Before &amp; after</a><a href="about.html">Our story</a><a href="blog.html">Blog</a><a href="faq.html">Patient FAQs</a></div>
<div><strong>Visit or book</strong><a href="contact.html">Clinic information</a><a href="tel:+{PHONE}">+92 321 5928003</a><a href="booking.html">Request an appointment</a><a href="privacy.html">Privacy</a></div>
<div><strong>Follow us</strong><a href="{INSTA}">Instagram ↗</a><a href="https://www.threads.com/@theladydentist.guj">Threads ↗</a><a href="{GOOGLE}">Google Business Profile ↗</a><a href="reviews.html">Patient reviews</a></div>
</div></footer>"""


def intro(label, title, description, action=""):
    return f"""<section class="sub-hero"><div class="wrap">
<a class="crumb" href="index.html">Home</a><p class="eyebrow"><span></span>{e(label)}</p>
<h1>{e(title)}</h1><p class="intro">{e(description)}</p>{action}</div></section>"""


def illustration(slug, after):
    """Draw a simplified treatment comparison as a local SVG asset."""
    name = f"{slug}-{'after' if after else 'before'}.svg"
    teeth = []
    for index in range(7):
        mid = index == 3
        if (slug in ("dental-implants", "dental-bridges") and mid and not after
                or slug == "tooth-extraction" and mid and after
                or slug == "dentures" and not after):
            continue
        x = 75 + index * 55
        y = 65 + abs(3 - index) * 6
        angle = 0
        if slug in ("braces", "clear-aligners") and not after:
            x += [0, -5, 4, -3, 8, -3, 0][index]
            y += [0, 8, -7, 13, -5, 8, 0][index]
            angle = [0, -10, 16, -20, 11, -7, 0][index]
        shade = "#e8c888" if slug == "teeth-whitening" and not after else "#fffaf2"
        path = "M-23 10 Q-25 -14 0 -16 Q24 -14 23 10 L19 46 Q17 61 0 62 Q-17 61 -19 46Z"
        if mid and slug in ("veneers", "dental-crowns") and not after:
            path = "M-23 10 Q-25 -14 0 -16 Q24 -14 23 10 L19 46 L6 52 L-3 41 L-11 56 Q-17 54 -19 46Z"
        marks = ""
        if slug == "scaling-polishing" and not after:
            marks = '<path d="M-20 3 Q-9 11 0 6 Q11 0 21 6" stroke="#aa742e" stroke-width="8" fill="none"/>'
        if mid and slug in ("fillings", "root-canal", "tooth-extraction"):
            fill = "#a95953" if not after else "#dfbfab"
            marks = f'<path d="M-5 1 Q0 -5 5 1 L5 32 Q0 39 -5 32Z" fill="{fill}"/>'
        if mid and slug == "dental-crowns" and after:
            marks = '<path d="M-22 12 Q0 5 22 12" stroke="#c7a99a" fill="none"/>'
        if mid and slug == "dental-implants" and after:
            marks = '<path d="M0 0v-34m-7 3 14 5m-14 2 14 5m-14 2 14 5" stroke="#637485" stroke-width="3"/>'
        teeth.append(f'<g transform="translate({x} {y}) rotate({angle})"><path d="{path}" fill="{shade}" stroke="#a77e79" stroke-width="2"/>{marks}</g>')
    overlay = ""
    if slug == "dental-checkup":
        overlay = '<circle cx="240" cy="95" r="31" fill="none" stroke="#a32861" stroke-width="3" stroke-dasharray="5 4"/>'
        if after:
            overlay += '<path d="m260 132 17 14 25-30" fill="none" stroke="#466a5b" stroke-width="5" stroke-linecap="round"/>'
    if slug == "dental-bridges" and after:
        overlay = '<path d="M175 112 H305" stroke="#aa847e" stroke-width="3" stroke-dasharray="4 4"/>'
    (ASSETS / name).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 185"><rect width="480" height="185" fill="#f8e3e7"/><path d="M0 72 Q240 -15 480 72 L480 0 H0Z" fill="#c87e8f"/>{"".join(teeth)}{overlay}</svg>',
        encoding="utf-8",
    )
    return name


def cards():
    return "".join(
        f'<article class="service catalog-card" data-category="{e(category)}">{picture(photo or slug + "-after.svg", f"Illustration for {name.lower()}")}<div><p class="category">{e(category)}</p><h3><a href="{slug}.html">{e(name)}</a></h3><p>{e(summary)}</p><a class="text-link" href="{slug}.html">Read the guide <span aria-hidden="true">→</span></a></div></article>'
        for slug, name, category, summary, *_, photo in GUIDES
    )


def filters():
    return '<div class="filters" data-filters aria-label="Filter by treatment category">' + "".join(
        f'<button type="button" data-filter="{name}" aria-pressed="{str(name == "All").lower()}">{name}</button>'
        for name in ("All", "Prevention", "Restorative", "Orthodontics", "Cosmetic")
    ) + '</div>'


def results():
    output = []
    for slug, name, category, *_, caption, photo in GUIDES:
        before = illustration(slug, False)
        after = illustration(slug, True)
        output.append(f"""<article class="service result-card" data-category="{category}" id="example-{slug}">
<div class="comparison" data-comparison>{picture(before, f"{name} before illustration")}{picture(after, f"{name} after illustration")}
<span class="before-label">Before</span><span class="after-label">After</span>
<label class="range-label"><span>Compare {e(name.lower())}</span><input type="range" min="0" max="100" value="50" aria-label="Compare before and after for {e(name.lower())}"></label></div>
<div><p class="category">Educational illustration</p><h3>{e(name)}</h3><p>{e(caption)}</p><a class="text-link" href="{slug}.html">Read treatment guide →</a></div></article>""")
    return "".join(output)


def reference_cases():
    references = (
        ("braces", "Braces", "Jeffrey Dorfman", "3.0", "Before_and_After_Photos_following_Orthodontic_Treatment_-_Teeth_Braces.jpg"),
        ("veneers", "Veneers", "Yvul", "4.0", "Faccette_estetiche_confronto_prima_e_dopo.jpg"),
    )
    return "".join(
        f'<figure class="reference-case">{picture(f"reference-{slug}.jpg", f"Before and after {title.lower()} from Wikimedia Commons")}<figcaption><strong>{title} · reference photo</strong><small>External case by <a href="https://commons.wikimedia.org/wiki/File:{source}">{author}</a> · <a href="https://creativecommons.org/licenses/by-sa/{license}/">CC BY-SA {license}</a></small></figcaption></figure>'
        for slug, title, author, license, source in references if (ASSETS / f"reference-{slug}.jpg").is_file()
    )


def treatment_pages():
    for slug, name, category, summary, needed, ages, steps, pain, cost, caption, photo in GUIDES:
        sections = (
            ("when", "When might I need it?", needed),
            ("ages", "What age group is it for?", ages),
            ("visit", "What happens at the appointment?", steps),
            ("comfort", "Does it hurt?", pain),
            ("cost", "How much does it cost?", cost),
        )
        links = "".join(f'<a href="#{anchor}">{title}</a>' for anchor, title, _ in sections)
        articles = "".join(f'<section id="{anchor}"><h2>{title}</h2><p>{e(copy)}</p></section>' for anchor, title, copy in sections)
        related = [f'<a href="{other_slug}.html">{e(other_name)} →</a>' for other_slug, other_name, group, *_ in GUIDES if group == category and other_slug != slug][:3]
        if not related:
            related = ['<a href="dental-checkup.html">Dental checkups →</a>']
        content = intro(category + " · Patient guide", name + " in Gujranwala", summary, button(whatsapp(name), "Ask about an appointment"))
        content += f"""<div class="wrap article-layout section">
<article class="article-copy"><figure class="article-photo">{picture(photo or slug + "-after.svg", f"Illustration for {name.lower()}")}
<figcaption>{"From The Lady Dentist’s clinic media" if photo else "Educational treatment illustration"}</figcaption></figure>
{articles}<p class="pricing-note">For current pricing and availability, ask the clinic for a quote in PKR based on your assessment.</p>
<div class="article-end"><h2>Plan your visit</h2><p>Ask the team about availability, the consultation fee, and what to bring. Wait for reception to confirm the date and time.</p>
{button(whatsapp(name), "Book on WhatsApp")} <a class="text-link" href="results.html#example-{slug}">See the illustration →</a></div>
<p class="source-note">General dental information: <a href="{NHS}">NHS dental treatments</a>.</p></article>
<aside class="article-aside"><strong>On this page</strong>{links}<a href="services.html">All treatment guides →</a><strong>Related treatments</strong>{"".join(related)}</aside></div>"""
        page(slug, name + " in Gujranwala", summary, content)


def clinic_gallery():
    photos = (
        ("google-reception.jpg", "Reception and clinic entrance hall"),
        ("google-lounge.jpg", "Waiting lounge"),
        ("google-surgery.jpg", "Dental treatment room"),
        ("google-exterior.jpg", "The Lady Dentist storefront on Main G.T. Road"),
    )
    available = [(name, alt) for name, alt in photos if (ASSETS / name).is_file()]
    if not available:
        available = [("clinic.webp", "Dental treatment room")]
    return '<div class="clinic-gallery">' + "".join(
        f'<figure>{picture(name, alt)}<figcaption>{e(alt)}</figcaption></figure>' for name, alt in available
    ) + '</div>'


def support_pages(home):
    page("about", "Our story", "Meet Dr. Asma Gull and see inside The Lady Dentist in Gujranwala.",
        intro("Our story", "Meet The Lady Dentist", "A Gujranwala dental practice led by Dr. Asma Gull, with care for patients at different stages of life.", button(whatsapp(), "Contact the clinic")) +
        f"""<section class="wrap section story-intro">{picture("doctor-portrait.webp", "Dr. Asma Gull")}
<div><p class="eyebrow"><span></span>DR. ASMA GULL, BDS</p><h2>A practice built around the visit.</h2><p>On Main G.T. Road, Dr. Asma and her team offer dental consultations with a focus on prevention, patient comfort, and clear conversations about treatment. The clinic shares practical dental education and behind-the-scenes videos with its Gujranwala community.</p><a class="text-link" href="{INSTA}">Follow the clinic on Instagram →</a></div></section>
<section class="wrap section"><h2>Meet the team</h2><figure class="team-panorama">{picture("team-wide.webp", "Dr. Asma Gull and five members of The Lady Dentist team")}</figure></section>
<section class="wrap section"><h2>Inside the clinic</h2>{clinic_gallery()}<a class="text-link" href="{GOOGLE}">Explore the Google photo listing →</a></section>""")
    page("contact", "Visit and contact", "Get directions to The Lady Dentist and contact the clinic on WhatsApp.",
        intro("Visit us", "Find us on Main G.T. Road", "Near Bank Al Habib and opposite Government Iqbal High School, Krishan Nagar, Gujranwala.", button(MAP, "Open Google Maps")) +
        f'<section class="wrap section"><div class="visit"><div><h2>Talk to reception</h2><p>Call or WhatsApp to check current opening hours and appointment availability before you travel.</p></div><div class="actions">{button(whatsapp(), "Message on WhatsApp")}<a class="text-link" href="tel:+{PHONE}">Call +92 321 5928003</a></div></div>{clinic_gallery()}</section>')
    questions = (
        ("How do I make an appointment?", "Use the WhatsApp button or call +92 321 5928003. Ask for a suitable time and wait for reception to confirm it."),
        ("Can I ask for a treatment price first?", "Yes. Ask for the consultation fee and whether imaging is separate. Treatment pricing may require an exam so the dentist can explain the options and total cost."),
        ("What should I bring?", "Bring any relevant records or X-rays you already have and a list of medications if applicable. Ask reception if anything else is required."),
        ("Can children visit?", "Ask reception about your child’s age and reason for the visit so they can arrange the appropriate appointment."),
        ("How can I change my appointment?", "Contact reception on the same WhatsApp number or by phone to agree a different time."),
        ("Can I check opening hours before travelling?", "Yes. Call or message the clinic for current hours and confirm your appointment before travelling."),
    )
    faq = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in questions)
    page("faq", "Patient FAQs", "Answers about appointments, pricing and visits to The Lady Dentist.",
         intro("Patient information", "Frequently asked questions", "What to know before you visit The Lady Dentist.") + f'<div class="wrap section faq-list">{faq}</div>')
    page("booking", "Request an appointment", "Open a WhatsApp appointment request with The Lady Dentist.",
         intro("Appointments", "Request a dental appointment", "Choose a reason for your visit and open WhatsApp. Reception will confirm the date and time with you.") +
         f'<section class="wrap section booking-layout"><form data-booking><label for="treatment">What would you like to discuss?</label><select id="treatment" name="treatment"><option value="">General appointment or unsure</option>{"".join(f"<option>{e(guide[1])}</option>" for guide in GUIDES)}</select><p>Your message stays in WhatsApp until you choose to send it.</p><a class="button" data-booking-link href="{whatsapp()}">Continue to WhatsApp →</a></form><aside><h2>Prefer to call?</h2><p><a class="text-link" href="tel:+{PHONE}">+92 321 5928003</a></p><p>Appointments are confirmed by reception.</p></aside></section>')
    page("privacy", "Privacy", "How this website handles appointment requests and external links.",
         intro("Website information", "Privacy", "This website provides clinic information and links for arranging a visit.") +
         '<div class="wrap section article-copy"><h2>Appointment requests</h2><p>The appointment page prepares a WhatsApp link on your device. This website does not submit or store the request. When you choose to send a message, WhatsApp and the clinic handle it through that service.</p><h2>External services</h2><p>Google Maps, Instagram, Threads and Google Fonts are external services. They apply their own privacy terms. For questions about clinic records or messages, contact the clinic directly.</p></div>')
    review = re.search(r'<section class="wrap section" id="reviews">.*?</section>', home, re.S).group()
    page("reviews", "Patient reviews", "Read excerpts from The Lady Dentist’s Google reviews.",
         intro("Patient experiences", "Patient reviews", "Read what patients shared about their visits to The Lady Dentist.") +
         review.replace('<svg><use href="#arrow"/></svg>', '<span aria-hidden="true">→</span>'))


def blog_pages():
    posts = [
        ("floss-or-toothpick", "Floss or toothpick?", "Daily care", "floss.webp", "DfEvMgKsVlG", "The clinic’s explainer looks at why it recommends floss for cleaning between teeth.",
         [("When food gets caught", "A toothpick can press into the gums. The clinic recommends floss to clean the space between teeth. If the same area traps food repeatedly, mention it at your next checkup."),
          ("Make it part of your routine", "Choose a time when you can clean between your teeth without rushing. If floss feels awkward or causes discomfort, ask the dental team to show you a technique or discuss another tool.")]),
        ("child-tooth-alignment", "When a child’s teeth come in crooked", "Family dentistry", "child.webp", "DfQNzD-siMy", "Dr. Asma discusses what parents can bring up at a child’s dental visit.",
         [("What to notice", "Note when the change began and mention any habits such as thumb sucking. Bring up problems with biting or changes you have seen as teeth come through."),
          ("What an assessment can clarify", "The dentist can look at how the teeth and bite are developing and explain whether monitoring or follow-up is appropriate. Timing depends on the child and the concern.")]),
        ("first-dental-visit", "Before your first dental visit", "Clinic life", "clinic.webp", "DdsYsPys7uw", "See the clinic and prepare a few questions before your first consultation.",
         [("Before you arrive", "Check the time with reception and save the map pin. The clinic is on Main G.T. Road near Bank Al Habib, opposite Government Iqbal High School."),
          ("What to ask at the consultation", "Explain what brought you in and ask about your options, whether imaging is needed, and what the proposed treatment would cost. Reception can clarify how follow-up is arranged.")]),
    ]
    cards = []
    for slug, title, category, image, reel, summary, sections in posts:
        cards.append(f'<article class="journal-card">{picture(image, title)}<div><p class="category">{category}</p><h3>{e(title)}</h3><p>{e(summary)}</p><a class="text-link" href="{slug}.html">Read article →</a></div></article>')
        body = "".join(f'<h2>{e(heading)}</h2><p>{e(copy)}</p>' for heading, copy in sections)
        page(slug, title, summary, intro(category + " · Clinic journal", title, summary) +
             f'<article class="wrap section article-copy standalone-article"><figure class="article-photo">{picture(image, title)}</figure>{body}<p><a class="text-link" href="{INSTA}reel/{reel}/">Watch the original clinic post →</a></p>{button(whatsapp(), "Ask about a checkup")}</article>')
    page("blog", "Clinic blog", "Dental tips and first-visit guides from The Lady Dentist.",
         intro("Clinic journal", "Dental care, explained.", "Read guides inspired by questions the clinic covers on Instagram.") +
         f'<div class="wrap section editorial-grid">{"".join(cards)}</div>')


def main():
    home_path = ROOT / "index.html"
    home = home_path.read_text(encoding="utf-8")
    result_cards = results()
    treatment_pages()
    page("services", "Dental treatments in Gujranwala", "Explore treatment guides with candidacy, comfort, costs and appointment links.",
        intro("Treatment library", "Explore dental treatments", "Learn what each treatment is for, what an appointment involves, and which questions to ask about cost. Check suitability and availability with the clinic.", button(whatsapp(), "Ask the clinic")) +
        f'<div class="wrap section">{filters()}<div class="care-grid catalog-grid" data-filter-grid>{cards()}</div></div>')
    references = reference_cases()
    reference_section = f'<section class="wrap section"><h2>Photographic references</h2><p>These openly licensed examples come from external sources.</p><div class="reference-grid">{references}</div></section>' if references else ""
    page("results", "Before and after gallery", "Compare educational before and after examples across dental treatments.",
         intro("Treatment gallery", "Before & after", "Compare educational diagrams and external reference photos. The examples illustrate possible changes and do not represent The Lady Dentist patients.") +
         reference_section + f'<section class="wrap section"><h2>Illustrated comparisons</h2><p>Move the slider to compare each stage.</p>{filters()}<div class="results-grid" data-filter-grid>{result_cards}</div></section>')
    support_pages(home)
    blog_pages()


if __name__ == "__main__":
    main()
