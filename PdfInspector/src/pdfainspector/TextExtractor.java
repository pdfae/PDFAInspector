package pdfainspector;
import java.io.IOException;

import nu.xom.Attribute;
import nu.xom.Element;

import com.itextpdf.text.pdf.PdfReader;
import com.itextpdf.text.pdf.parser.PdfReaderContentParser;
import com.itextpdf.text.pdf.parser.SimpleTextExtractionStrategy;
import com.itextpdf.text.pdf.parser.TextExtractionStrategy;

/**
 * Convert text in a PDF to a XOM XML element.
 * @author schiele1
 */
public class TextExtractor {

	/**
	 * Given an iText PDF Reader, extract text from the PDF and store it in a
	 * XOM XML element.
	 * @param reader A reader for the given PDF.
	 * @return A XOM element containing the text.
	 */
	public static Element extractToXML(PdfReader reader){
    	Element root = new Element("Text");
    	
    	// Set up iText's PDF text extraction tools.
    	PdfReaderContentParser parser = new PdfReaderContentParser(reader);
    	TextExtractionStrategy strategy = new SimpleTextExtractionStrategy();
    	// Make an element for each page of text, labeled with the page number.
    	for (int i = 1; i <= reader.getNumberOfPages(); i++) {
    		try{
    			// There are several different extraction strategies available.
    			strategy = parser.processContent(i, new SimpleTextExtractionStrategy());
    			//strategy = parser.processContent(i, new LocationTextExtractionStrategy());
    		}catch(IOException e){}
    		String result = strategy.getResultantText();
    		
    		// If there's text on the page, label it and add it to the root.
    		if(result != null){
    			Element page = new Element("Plaintext");
    			page.addAttribute(new Attribute("Page", Integer.toString(i)));
    			page.appendChild(result);
    			root.appendChild(page);
    		}
    	}
    	return root;
	}
}
