from urllib import parse, request
import webbrowser


def post_image():
    path = "D://DQE//10reasons.jpg"  # path to image
    url = 'http://localhost:8080/showimage'
    parms = {'image': path}

    querystring = parse.urlencode(parms)
    print(querystring)

    u = request.urlopen(url + '?' + querystring)
    return u.read()


def name_get():
    url = 'http://localhost:8080/hello'
    parms = {'name': 'Nazar'}
    querystring = parse.urlencode(parms)
    print(querystring)
    u = request.urlopen(url + '?' + querystring)
    return (u.read())


if __name__ == '__main__':
    html_code = post_image()
    print(html_code)
    with open("../html_req.html", "w") as f:
        f.write(str(html_code).replace('\\n', ''))  # haven't found solution to get ridding of newlines
                                                    # (encoding restricted)
    webbrowser.open_new_tab(f.name)  # open html file in browser
