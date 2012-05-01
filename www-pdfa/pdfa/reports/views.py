'''
The "reports" app parses the Tag tree/ results to render different views ->
1) Summary: a compiled summary of all evaluations
2) Tag tree: rendered view of the tag tree
3) Links: link tag specific evaluations
4) Figures: figure tag specific evaluations
5) Forms: form control specific evaluations
6) Headers: header tag specific evaluations
7) Tables: table specific evaluations
8) Bookmarks: bookmark specific evaluations
9) Empty tags: list of empty tags
'''

# including required modules
from django.shortcuts import *
from settings import *
from django.contrib.auth.decorators import login_required
import os
from backends import *
import json
from upload.models import UserFile
from upload.forms import notesupdateform

'''
get metadata info from parsed tag tree
'''
def getmetadata(parsedata):
    for c in parsedata['content']:
        if c["tagName"] == "Metadata":
            metadata = c["content"]
        if c["tagName"] == "tags":
            tagged = len(c["content"]) > 0
    for m in metadata:
        if m["tagName"] == "Title":
            mettitle = m["content"]
        if m["tagName"] == "Pages":
            numpages = m["content"]
        if m["tagName"] == "Language":
            language = m["content"]
    return [tagged, mettitle, numpages, language]

'''
initialize rule levels
'''
def init(levels):
    for i in range(7):
        levels.append({})
        levels[i]['tests'] = []
    levels[0]['title'] = "Link Tags"
    levels[1]['title'] = "Figure (Image) Tags"
    levels[2]['title'] = "Heading Tags"
    levels[3]['title'] = "Table Tags"
    levels[4]['title'] = "Empty Tags"
    levels[5]['title'] = "Form Controls"
    levels[6]['title'] = "Bookmarks"

'''
(displaysummary) <- method to render summary page
args:
    request <- Http request
    uid <- unique report id
django template variables:    
    tagged <- is document tagged
    mettitle <- document title
    numpages <- number of pages in document
    headed <- does document have headers
    language <- document language
    numtags <- total number of tags
    tot_fail <- total violations
    tot_war <- total warnings
    tot_ins <- total manual checks
    levels <- different sets of rules each with title and list of rules
'''
def displaysummary(request, uid):
    
    # obtain template variables
    currentTab = "summary"
    [auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
    
    # if results are done processing
    if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):    
        
        # get tag tree and results as Python objects
        resultFP = open(resultfile)
        result_data = json.load(resultFP)
        resultFP.close()
        parseFP = open(parsefile)
        parse_data = json.load(parseFP)
        parseFP.close()
        
        #extract document accessibility information -> tagged, mettitle, numpages, language
        [tagged, mettitle, numpages, language] = getmetadata(parse_data)
        
        #extract tag accessibility -> evaluation summary
        tests = result_data["results"]
        levels = []
        
        #initialize
        init(levels)
        tot_fail = 0
        tot_war = 0
        tot_ins = 0
        numtags = 0
        
        #for every test run, extract information for rendering
        for test in tests:
            # count violations, warnings and manual checks for each test
            test['nfail'] = 0
            test['nins'] = 0
            test['nwar'] = 0
            for tag in test["tags"]:
                if tag['result'] == 2:
                    test['nfail'] += 1
                elif tag['result'] == 3:
                    test['nins'] += 1
                elif tag['result'] == 4:
                    test['nwar'] += 1
            
            if test["category"] == 1:
                #link tag rules
                levels[0]['num'] = len(test["tags"])
                levels[0]['tests'].append(test)
            elif test["category"] == 2:
                #figure tag rules
                levels[1]['num'] = len(test["tags"])
                numtags += len(test["tags"])
                levels[1]['tests'].append(test)
            elif test["category"] == 3:
                #form control rules
                levels[5]['num'] = len(test["tags"])
                levels[5]['tests'].append(test)  
            elif test["category"] == 4:
                #heading rules
                if test["id"] == "core.HeadingsMustContainTextContent":
                    #num of headings = num of tags tested by this rule
                    levels[2]['num'] = len(test["tags"])
                levels[2]['tests'].append(test)
            elif test["category"] == 5:
                #table rules
                if test["id"] == "core.TablesMustHaveHeadings":
                    #num of tables = num of tags tested by this rule
                    levels[3]['num'] = len(test["tags"])
                levels[3]['tests'].append(test)
            elif test["category"] == 6:
                #bookmark rules 
                levels[6]['num'] = len(test["tags"])
                levels[6]['tests'].append(test)
            if test["id"] == "core.NonFigureTagsMustContainContent":
                #empty tags
                levels[4]['num'] = test['nwar']
                levels[4]['tests'].append(test)
                numtags += len(test["tags"])
            
            #total statistics
            tot_fail += test['nfail']
            tot_war += test['nwar']
            tot_ins += test['nins']
        
        #headings exist if num of headings greater than 0
        headed = levels[2]['num'] > 0    
        
        #accessibility notes form
        form = setup_notes_form(request, uid, notes, fileObj)
        return render_to_response("reports/summaryview.html", locals(), context_instance=RequestContext(request))
    else:
        return render_to_response("reports/summary_notfound.html", locals())

def setup(user, uid):
    auth = user.is_authenticated()
    if auth:
        currentPage = "reports"
    else:
        currentPage = "upload"
    fileObj = UserFile.objects.get(uid=uid)
    title = fileObj.title
    notes = fileObj.notes
    [filepath, filename] = fileObj.file.name.rsplit('/', 1)
    filepath = MEDIA_ROOT + filepath + "/"
    parsefile = filepath + "json-" + filename.replace('.pdf', '') + ".json"
    resultfile = filepath + "result-" + filename.replace('.pdf', '') + ".json"
    return [auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename]

def setup_notes_form(request, uid, notes, fileObj):
    if (request.method == "POST"):
            form = notesupdateform(request.POST)
            if form.is_valid():
                fileObj = UserFile.objects.get(uid=uid)
                fileObj.notes = form.cleaned_data['notes']
                fileObj.save()
    else:
        data = {'notes': notes}
        form = notesupdateform(data)
    return form
    
# tab to display tree view

def displaytreeview(request, uid):
    currentTab = "tree"
    [auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
    if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):    
        tags = "<div class=\"css-treeview\">"
        tags += writeTag(parsefile, "tags")
        tags += "</div>"
        tags += "<div class=\"css-treeview\">"
        tags += writeTag(parsefile, "Form", "No forms found.")
        tags += "</div>"
        return render_to_response("reports/treeview.html", locals())
    else:
        return render_to_response("reports/summary_notfound.html", locals())

def displaylinks(request, uid):
    currentTab = "links"
    [auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
    if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):    
        name = "Link"
        info = "Text"
        [ruleRows, tagged, num, numfail] = getData(parsefile, resultfile, uid, 1, name)
        return render_to_response("reports/rowView.html", locals())
    else:
        return render_to_response("reports/summary_notfound.html", locals())

def displayfigures(request, uid):
    currentTab = "img"
    [auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
    if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):    
        name = "Figure"
        info = "Alt Text"
        [ruleRows, tagged, num, numfail] = getData(parsefile, resultfile, uid, 2, name)
        return render_to_response("reports/rowView.html", locals())
    else:
        return render_to_response("reports/summary_notfound.html", locals())

def displayforms(request, uid):
    currentTab = "form"
    [auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
    if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):    
        name = "Form Control"
        info = "Tooltip"
        [ruleRows, tagged, num, numfail] = getData(parsefile, resultfile, uid, 3, name)
        return render_to_response("reports/formview.html", locals())
    else:
        return render_to_response("reports/summary_notfound.html", locals())

def displayhead(request, uid):
    currentTab = "head"
    [auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
    if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):    
        name = "Header"
        info = "Text"
        [ruleRows, tagged, num, numfail] = getData(parsefile, resultfile, uid, 4, name)
        return render_to_response("reports/headerview.html", locals())
    else:
        return render_to_response("reports/summary_notfound.html", locals())

def displaybookmark(request, uid):
    currentTab = "bm"
    [auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
    if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):    
        tags = "<div class=\"css-treeview\">"
        tags += writeBkTag(parsefile, "Bookmarks")
        tags += "</div>"
        return render_to_response("reports/treeview.html", locals())
    else:
        return render_to_response("reports/summary_notfound.html", locals())

def displaytables(request, uid):
    currentTab = "tbl"
    [auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)    
    if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):    
        [ruleRows, tagged, num, output] = getTable(parsefile, resultfile)
        name = "table"
        return render_to_response("reports/tableview.html", locals())
    else:
        return render_to_response("reports/summary_notfound.html", locals())

def displayempty(request, uid):
    currentTab = "empty"
    [auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)    
    if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):    
        resultFP = open(resultfile)
        result_data = json.load(resultFP)
        resultFP.close()
        parseFP = open(parsefile)
        parse_data = json.load(parseFP)
        parseFP.close()
        tests = result_data["results"]
        numwar = 0
        empty = []
        tagged = False
        tag_urls = {}
        title2 = ""
        getNodes(parse_data, 0, tag_urls)
        for test in tests:
            if test["id"] == "core.DocumentMustBeTagged" and test['tags'][0]['result'] == 1:
                tagged = True
            if test["id"] == "core.NonFigureTagsMustContainContent":    
                title2 = test["title"]
                numbering = {}
                for tag in test["tags"]:
                    actual_tag = tag_urls[tag['tag']]
                    tag['tagName'] = actual_tag['tagName']
                    tN = actual_tag['tagName']
                    if tN in numbering:
                        numbering[tN] += 1
                    else:
                        numbering[tN] = 1
                    tag['level'] = unicode(numbering[tN])    
                    if tag['result'] == 4:
                        numwar += 1
                        
                        attr = []
                        if 'attributes' in actual_tag:
                            attr = actual_tag['attributes']
                        for a in attr:
                            if 'Page' in a:
                                tag['page'] = a['Page']
                        empty.append(tag)
        return render_to_response("reports/emptyview.html", locals())
    else:
        return render_to_response("reports/summary_notfound.html", locals())
        
def displayformtree(request, uid):
    currentTab = "formtree"
    [auth, currentPage, parsefile, resultfile, title, notes, fileObj, filename] = setup(request.user, uid)
    if (os.path.isfile(parsefile) and os.path.isfile(resultfile)):    
        result = open(parsefile)
        base = json.loads(result.read())
        output = '<a href="javascript:check_all()">Expand All</a>'
        output += '&nbsp&nbsp&nbsp&nbsp&nbsp<a href="javascript:uncheck_all()">Collapse All</a>'
        output += "<div class=\"css-treeview\">"
        output += writeNode2(base, "Form")
        output += "</div>"
        return render_to_response("reports/treeview.html", locals())
    else:
        return render_to_response("reports/summary_notfound.html", locals())
