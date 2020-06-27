import flask
import sys
from CompanySiteToJson import Ext
from flask import request, jsonify
from numba import jit, prange
import Keywordsext as ke
import traceback
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:

    sys.path.insert(0, '')

    app = flask.Flask(__name__)
    app.config["DEBUG"] = True


    @jit
    @app.route('/urlsearch', methods=['GET'])
    def api_urlsearch():
        # Check if an ID was provided as part of the URL.
        # If ID is provided, assign it to a variable.
        # If no ID is provided, display an error in the browser.

        if 'id' in request.args:
            idu = request.args['id']
        else:
            return "Error: No id field provided. Please specify an id."

        if idu.startswith("https://") or idu.startswith("http://") and "." in idu:

            obj = Ext(idu)
            urllist = obj.findlinks()

            if urllist is None:
                sys.exit()
            urllist.append(idu)

            my_objects = []

            for i in prange(len(urllist)):
                my_objects.append(Ext(urllist[i]))
                my_objects[i].extract()

            printdict = obj.printing()

            objnlpapp = ke.Nlpapp(urllist)
            keylist = objnlpapp.topwords()

            printdict['keywords'] = keylist
            printdict['important links'] = list(dict.fromkeys(urllist))
            del obj
            del my_objects
            return jsonify(printdict)

        else:
            del obj
            errdict={}
            errdict['error message'] = "bad url"
            return jsonify(errdict)

    @app.route('/emailsearch', methods=['GET'])
    def api_emailsearch():
        # Check if an ID was provided as part of the URL.
        # If ID is provided, assign it to a variable.
        # If no ID is provided, display an error in the browser.

        if 'id' in request.args:
            idemail = request.args['id']
        else:
            return "Error: No id field provided. Please specify an id."

        if "@" in idemail and "." in idemail:

            indexemail = idemail.find('@')
            dom = idemail[(indexemail+1):len(idemail)]
            idu = "http://www." + dom

            obj = Ext(idu)
            urllist = obj.findlinks()

            if urllist is None:
                sys.exit()
            urllist.append(idu)

            my_objects = []

            for i in prange(len(urllist)):
                my_objects.append(Ext(urllist[i]))
                my_objects[i].extract()

            printdict = obj.printing()

            objnlpapp = ke.Nlpapp(urllist)
            keylist = objnlpapp.topwords()

            printdict['keywords'] = keylist
            printdict['important links'] = list(dict.fromkeys(urllist))
            del obj
            del my_objects
            return jsonify(printdict)

        else:
            del obj
            errdict = {}
            errdict['error message'] = "bad url"
            return jsonify(errdict)

    app.run()

except KeyboardInterrupt:
    raise

except Exception as error:
    traceback.print_exc()
    logger.debug(traceback.format_exc())
    desired_trace = traceback.format_exc(sys.exc_info())
    logger.debug(desired_trace)
