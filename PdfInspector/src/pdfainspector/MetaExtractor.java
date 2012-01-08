package pdfainspector;
import java.util.HashMap;

import nu.xom.Element;

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
    	
    	// Make an element for it...
    	Element root = new Element("Metadata");
    	Element titleElement = new Element("Title");
    	Element authorElement = new Element("Author");
    	Element creatorElement = new Element("Creator");
    	Element pagesElement = new Element("Pages");
    	
    	// Add the retrieved data to the corresponding element...
    	titleElement.appendChild(title);
    	authorElement.appendChild(author);
    	creatorElement.appendChild(creator);
    	pagesElement.appendChild(pages);
    	
    	// And add each element to the root, which we return.
    	root.appendChild(titleElement);
    	root.appendChild(authorElement);
    	root.appendChild(creatorElement);
    	root.appendChild(pagesElement);
    	
    	return root;
	}
}