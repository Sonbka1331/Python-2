from flask import Flask, url_for

app = Flask(__name__)


@app.route('/test')
def test():
    return 'test'


@app.route('/test_2')
def test_2():
    return 'test_2'


@app.route('/test_3')
def test_3():
    return 'test_3'


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.errorhandler(404)
def page_not_found(e):
    urls = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            urls.append((url, rule.endpoint))
    return urls, 404


if __name__ == "__main__":
    app.run()
