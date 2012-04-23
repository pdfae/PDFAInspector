package pdfainspector;
import java.util.HashMap;

import nu.xom.Element;

import com.itextpdf.text.pdf.PdfDictionary;
import com.itextpdf.text.pdf.PdfName;
import com.itextpdf.text.pdf.PdfReader;

/**
 * Convert metadata in a PDF to a XOM XML element.
 * @author schiele1
 */
public class MetaExtractor {
	
	/**
	 * Given an iText PDF Reader, extract metadata from the PDF and store it in
	 * a XOM XML element.
	 * @param reader A reader for the given PDF.
	 * @return A XOM element containing metadata.
	 */
	public static Element extractToXML(PdfReader reader){
		
		// For each desired metadata item, retrieve it from the document...
		HashMap<String,String> metadata = reader.getInfo();
    	String title = metadata.get("Title");
    	String author = metadata.get("Author");
    	String creator = metadata.get("Creator");
    	String pages = Integer.toString(reader.getNumberOfPages());

    	// Language data is stored somewhere else
    	String language = "None";
		PdfDictionary catalog = reader.getCatalog();
		if(catalog.contains(PdfName.LANG)){
				language = sanitize(catalog.getAsString(PdfName.LANG).toString());
		}
		if(language == ""){
			language = "None";
		}
    	
    	// Make an element for it...
    	Element root = new Element("Metadata");
    	Element titleElement = new Element("Title");
    	Element authorElement = new Element("Author");
    	Element creatorElement = new Element("Creator");
    	Element pagesElement = new Element("Pages");
    	Element languageElement = new Element("Language");
    	
    	// Add the retrieved data to the corresponding element...
    	titleElement.appendChild(title);
    	authorElement.appendChild(author);
    	creatorElement.appendChild(creator);
    	pagesElement.appendChild(pages);
    	languageElement.appendChild(language);
    	
    	// And add each element to the root, which we return.
    	root.appendChild(titleElement);
    	root.appendChild(authorElement);
    	root.appendChild(creatorElement);
    	root.appendChild(pagesElement);
    	root.appendChild(languageElement);
    	
    	return root;
	}
	
	/**
	 * Remove all null characters from a string so we can put it into XML.
	 * @param dict The string to sanitize.
	 * @return The sanitized string (i.e. with all null chars removed).
	 */
    private static String sanitize(String input){
    	if(input.startsWith("\u00fe\u00ff")){
    		input = input.substring(2);
    	}
		String sanitized = "";
		for(int i = 0; i < input.length(); i++){
			char c = input.charAt(i);
			if(c != '\0'){
				sanitized = sanitized + c;
			}
		}
		return sanitized;
    }
}
