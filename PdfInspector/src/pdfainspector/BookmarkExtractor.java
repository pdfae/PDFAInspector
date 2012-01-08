package pdfainspector;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import nu.xom.Attribute;
import nu.xom.Element;

import com.itextpdf.text.pdf.PdfReader;
import com.itextpdf.text.pdf.SimpleBookmark;
import com.itextpdf.text.pdf.SimpleNamedDestination;

/**
 * Convert PDF bookmark data into a XOM XML element. This code is based loosely
 * on the SimpleBookmark class from iText 5.1.3, but heavily modified to
 * incorporate XOM elements.
 * @author schiele1
 */
public class BookmarkExtractor {
	
	/**
	 * Given an iText PDF Reader, extract bookmark data from the PDF and store
	 * it in a XOM XML element.
	 * @param reader A reader for the given PDF.
	 * @return A XOM element containing bookmark data.
	 */
	public static Element extractToXML(PdfReader reader){
		Element root = new Element("Bookmarks");
		// Get the bookmark data from the reader.
		List<HashMap<String,Object>> list = SimpleBookmark.getBookmark(reader);

		// Get elements for each top-level bookmark, which will also contain
		// data for all its child bookmarks.
		List<Element> bookmarks = bookmarkHelper(list);
		
		// Then append them all to a single root element.
		if(bookmarks != null){
			for(Element bookmark : bookmarks){
				root.appendChild(bookmark);
			}
		}

		return root;
	}
	
	/**
	 * Convert each bookmark in the input list into a XOM element, and
	 * recursively include all of its children as sub-elements.
	 * @param list A list of all the bookmarks on this level.
	 * @return A list of elements, one for each bookmark in the parameter list.
	 */
	private static List<Element> bookmarkHelper(List<HashMap<String,Object>> list){
        ArrayList<Element> bookmarks = new ArrayList<Element>();
        if (list == null){
        	return bookmarks;
        }
        
        for(HashMap<String, Object> map : list){
            List<HashMap<String, Object>> kids = null;
            Element title = new Element("Title");
            
            // Iterate through all the keys in the Bookmark structure and add
            // them as attributes to the XOM element. Also get the child list.
            for(Map.Entry<String, Object> entry : map.entrySet()){
                String key = entry.getKey();
                
                if(key.equals("Title")){
                    title.appendChild((String)entry.getValue());
                }
                
                else if (key.equals("Kids")){
                    kids = (List<HashMap<String, Object>>)entry.getValue();
                }
                
                else{
                	String value = (String)entry.getValue();
                	if (key.equals("Named") || key.equals("NamedN")){
                        value = SimpleNamedDestination.escapeBinaryString(value);
                	}
                    title.addAttribute(new Attribute(key, value));
                }
            }
            
            // Recursively generate XOM elements for children of this bookmark.
            if (kids != null){
            	List<Element> children = bookmarkHelper(kids);
            	for(Element child : children){
            		title.appendChild(child);
            	}
            }
            
            bookmarks.add(title);
        }
        
        return bookmarks;
	}
}
