



def split_into_stripes_and_lines(html_str, process_cb):
    html_stripes = html_str.split("<br><br>")
    processed_html_stripes = []
    for html_stripe in html_stripes:
        html_lines = html_stripe.split("<br>")
        processed_stripe_lines = []
        for html_line in html_lines:
            processed_html_line = process_cb(html_line)
            if processed_html_line:
                processed_stripe_lines.append(processed_html_line)
        processed_stripe = "<br>".join(processed_stripe_lines)
        if processed_stripe:
            processed_html_stripes.append(processed_stripe)
    processed_html_str = "<br><br>".join(processed_html_stripes)
    return processed_html_str