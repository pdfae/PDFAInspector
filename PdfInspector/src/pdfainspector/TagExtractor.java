package pdfainspector;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import nu.xom.Attribute;
import nu.xom.Element;

import com.itextpdf.text.pdf.PdfArray;
import com.itextpdf.text.pdf.PdfDictionary;
import com.itextpdf.text.pdf.PdfName;
import com.itextpdf.text.pdf.PdfNumber;
import com.itextpdf.text.pdf.PdfObject;
import com.itextpdf.text.pdf.PdfReader;
import com.itextpdf.text.pdf.parser.FilteredTextRenderListener;
import com.itextpdf.text.pdf.parser.MarkedContentRenderFilter;
import com.itextpdf.text.pdf.parser.PdfContentStreamProcessor;
import com.itextpdf.text.pdf.parser.RenderFilter;
import com.itextpdf.text.pdf.parser.SimpleTextExtractionStrategy;
import com.itextpdf.text.pdf.parser.TextExtractionStrategy;

/**
 * Convert tag data in a PDF to a XOM XML element. This is based loosely on the
 * TaggedPdfReaderTool from iText 5.1.3, and very heavily modified to include
 * desired features, such as page numbers, attributes, and XOM elements.
 * @author schiele1
 */
public class TagExtractor {

	/**
	 * Given an iText PDF Reader, extract tag data from the PDF and store it in
	 * a XOM XML element.
	 * @param reader A reader for the given PDF.
	 * @return A XOM element containing tag data.
	 */
	public static Element extractToXML(PdfReader reader){
		Element root = new Element("tags");
		
		// Find the root of the tag structure tree
		PdfDictionary catalog = reader.getCatalog();
		if(!catalog.contains(PdfName.STRUCTTREEROOT)){
			return root;
		}
		PdfDictionary structTree = catalog.getAsDict(PdfName.STRUCTTREEROOT);
		
		// Parse the tag tree into XOM elements then add them to the root.
		List<Element> tags = parseChild(structTree.getDirectObject(PdfName.K));
		if(tags != null){
			for(Element tag : tags){
				root.appendChild(tag);
			}
		}
		return root;
	}
	
	/**
	 * Wrapper function for parsing a PDF Object, passes it to either the array
	 * or the dictionary parser and returns the list those parsers output.
	 * @param child The PdfObject to be parsed.
	 * @return The list of XOM elements representing that object.
	 */
    private static List<Element> parseChild(PdfObject child){
    	List<Element> tags = new ArrayList<Element>();
		if(child != null){
			if (child instanceof PdfArray){
				tags = parseArray((PdfArray) child);
			}
			else if (child instanceof PdfDictionary){
				tags = parseDictionary((PdfDictionary) child);
			}
		}
		return tags;
    }
    
    /**
     * Parse each object in the given PdfArray into a list of XOM elements,
     * then append them all to a master list of elements representing the array.
     * @param array The PdfArray to be parsed.
     * @return A list of XOM elements representing the combination of every
     * PdfObject in the array.
     */
    private static List<Element> parseArray(PdfArray array){
    	List<Element> tags = new ArrayList<Element>();
    	
		if(array != null){
			for (int i = 0; i < array.size(); i++) {
				List<Element> childList = parseChild(array.getDirectObject(i));
				if(childList != null){
					tags.addAll(childList);
				}
			}
		}
		
		return tags;
    }
    
    /**
     * A dictionary will either directly contain tag data, or it will contain
     * references to other objects which may contain the data. This is where
     * the bulk of the parsing work is done.
     * @param dict The PdfDictionary to be parsed.
     * @return A list of elements corresponding to the tag data contained in
     * the dictionary and/or its children.
     */
    private static List<Element> parseDictionary(PdfDictionary dict){
    	List<Element> tags = new ArrayList<Element>();
		if(dict != null){
			// If the dict contains tag data, we need to extract it.
			PdfName tagString = dict.getAsName(PdfName.S);
			if (tagString != null) {
				// Decode the tag name and make a XOM element with that name.
	            String tagDecode = PdfName.decodeName(tagString.toString());
				String tagName = fixTagName(tagDecode);
				Element tag = new Element(tagName);
				
				// Fetch the tag attributes (including page numbers and alt
				// text), and add them to the tag element.
				List<Attribute> attributes = extractAttributes(dict);
				for(Attribute attribute : attributes){
					tag.addAttribute(attribute);
				}

				// Then, read in the actual contents of the tag.
				PdfDictionary page = dict.getAsDict(PdfName.PG);
				String contents = null;
				if (page != null){
					contents = parseTag(tagDecode, dict.getDirectObject(PdfName.K), page);
				}
				if(contents != null){
					tag.appendChild(contents);
				}
				
				// If the tag has children, we need to parse them, too.
				List<Element> childList = parseChild(dict.getDirectObject(PdfName.K));
				if(childList != null){
					for(Element element : childList){
						tag.appendChild(element);
					}
				}
				
				// Once we've done all that, we return our finished element.
				tags.add(tag);
			}
			
			// If the dict is not a tag, we need to dig deeper into it to find
			// the tag data we need.
			else {
				tags = parseChild(dict.get(PdfName.K));
			}
		}
    	return tags;
    }
    
    /**
     * Taken from iText's TaggedPdfReaderTool, this renders tag name codes into
     * a human readable format.
     * @param tag The tag to format.
     * @return A human-readable string representing the tag name.
     */
    private static String fixTagName(String tag) {
        StringBuilder sb = new StringBuilder();
        for (int k = 0; k < tag.length(); ++k) {
            char c = tag.charAt(k);
            boolean nameStart =
                c == ':'
                || (c >= 'A' && c <= 'Z')
                || c == '_'
                || (c >= 'a' && c <= 'z')
                || (c >= '\u00c0' && c <= '\u00d6')
                || (c >= '\u00d8' && c <= '\u00f6')
                || (c >= '\u00f8' && c <= '\u02ff')
                || (c >= '\u0370' && c <= '\u037d')
                || (c >= '\u037f' && c <= '\u1fff')
                || (c >= '\u200c' && c <= '\u200d')
                || (c >= '\u2070' && c <= '\u218f')
                || (c >= '\u2c00' && c <= '\u2fef')
                || (c >= '\u3001' && c <= '\ud7ff')
                || (c >= '\uf900' && c <= '\ufdcf')
                || (c >= '\ufdf0' && c <= '\ufffd');
            boolean nameMiddle =
                c == '-'
                || c == '.'
                || (c >= '0' && c <= '9')
                || c == '\u00b7'
                || (c >= '\u0300' && c <= '\u036f')
                || (c >= '\u203f' && c <= '\u2040')
                || nameStart;
            if (k == 0) {
                if (!nameStart)
                    c = '_';
            }
            else {
                if (!nameMiddle)
                    c = '-';
            }
            sb.append(c);
        }
        return sb.toString();
    }
    
    /**
     * Use iText's text parsing tools to read the text inside the given tag. It
     * scans the given page dictionary to find the start of the tag, and reads
     * all the text until it finds the end of the tag.
     * @param tag The tag type to search for on the page.
     * @param object The actual tag object we are parsing (the "K" element of
     * the parent PdfDictionary).
     * @param page The dictionary representing the page on which the tag starts.
     * @return A string containing the text within the given tag.
     */
	private static String parseTag(String tag, PdfObject object, PdfDictionary page){
		// If object is a number, then it is the Marked Content ID of the tag
		// we're looking for, and we can jump to that tag on the page.
		if (object instanceof PdfNumber) {
			PdfNumber mcid = (PdfNumber) object;
			// The filter will only search for text corresponding to the MCID.
			RenderFilter filter = new MarkedContentRenderFilter(mcid.intValue());
			TextExtractionStrategy strategy = new SimpleTextExtractionStrategy();
			FilteredTextRenderListener listener = new FilteredTextRenderListener(
					strategy, filter);
			PdfContentStreamProcessor processor = new PdfContentStreamProcessor(listener);
			try{
				processor.processContent(PdfReader.getPageContent(page), page.getAsDict(PdfName.RESOURCES));
			}catch(IOException e){
				return "";
			}
			return listener.getResultantText();
		}

		// If object is an array, we can search for tags within each element.
		else if (object instanceof PdfArray) {
			PdfArray arr = (PdfArray) object;
			int n = arr.size();
			String text = "";
			for (int i = 0; i < n; i++) {
				text = text + parseTag(tag, arr.getPdfObject(i), page);
				if (i < n - 1)
					text = text + "\n";
			}
			return text;
		}

		// If it's a dictionary, we can simply parse its MCID element.
		else if (object instanceof PdfDictionary) {
			PdfDictionary mcr = (PdfDictionary) object;
			return parseTag(tag, mcr.getDirectObject(PdfName.MCID), mcr.getAsDict(PdfName.PG));
		}
		
		// We should never reach here.
		else{
			return "";
		}
	}
	
	/**
	 * Search a tag dictionary for attributes and return a list of them.
	 * @param dict The tag dictionary to search.
	 * @return A list of all the attributes found.
	 */
    private static List<Attribute> extractAttributes(PdfDictionary dict){
    	ArrayList<Attribute> attributes = new ArrayList<Attribute>();
    	
    	// To find the page number, first get the page dictionary.
    	PdfDictionary page = dict.getAsDict(PdfName.PG);
    	int pageNumber = 0;
		if(page != null){
			// ...then search for it in the master list of pages.
			PdfArray pages = page.getAsDict(PdfName.PARENT).getAsArray(PdfName.KIDS);
			for(int i = 0; i < pages.length(); i ++){
				if(page == pages.getAsDict(i)){
					pageNumber = i + 1;
					break;
				}
			}
		}
		attributes.add(new Attribute("Page", Integer.toString(pageNumber)));
		
		// If there's an alt-text, get it.
		if (dict.get(PdfName.ALT) != null){
			String alt = dict.get(PdfName.ALT).toString();
			
			// All alt-texts contain null characters. We can't have those.
			String altText = "";
			for(int i = 0; i < alt.length(); i++){
				char c = alt.charAt(i);
				if(c != '\0'){
					altText = altText + c;
				}
			}

			attributes.add(new Attribute("Alt", altText));
		}
    	
		// Some tags, such as table elements, may have IDs.
		if(dict.get(PdfName.ID) != null){
			String id = dict.get(PdfName.ID).toString();
			attributes.add(new Attribute("ID", id));
		}
		
		// The rest of the attributes are contained in a dictionary. We can
		// pull out the ones we want here.
		PdfDictionary a = dict.getAsDict(PdfName.A);
    	if (a != null){
    		
    		PdfObject summary = a.get(new PdfName("Summary"));
    		PdfObject scope = a.get(new PdfName("Scope"));
    		PdfObject header = a.get(new PdfName("Headers"));
    		PdfObject rowspan = a.get(new PdfName("RowSpan"));
    		PdfObject colspan = a.get(new PdfName("ColSpan"));

    		if (summary != null){
    			attributes.add(new Attribute("Summary", summary.toString()));
    		}
    		if (scope != null){
    			attributes.add(new Attribute("Scope", scope.toString()));
    		}
    		if (header != null){
    			attributes.add(new Attribute("Headers", header.toString()));
    		}
    		if (rowspan != null){
    			attributes.add(new Attribute("RowSpan", rowspan.toString()));
    		}
    		if (colspan != null){
    			attributes.add(new Attribute("ColSpan", colspan.toString()));
    		}    		
    	}
    	return attributes;
    }
}