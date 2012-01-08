package pdfainspector;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import nu.xom.Attribute;
import nu.xom.Element;

import com.itextpdf.text.pdf.PdfName;
import com.itextpdf.text.pdf.PdfNumber;
import com.itextpdf.text.pdf.PdfReader;
import com.itextpdf.text.pdf.parser.ImageRenderInfo;
import com.itextpdf.text.pdf.parser.PdfReaderContentParser;
import com.itextpdf.text.pdf.parser.RenderListener;
import com.itextpdf.text.pdf.parser.TextRenderInfo;

/**
 * Convert image data in a PDF to a XOM XML element.
 * @author schiele1
 */
public class ImageExtractor {

	/**
	 * Given an iText PDF Reader, extract image data from the PDF and store it
	 * in a XOM XML element.
	 * @param reader A reader for the given PDF.
	 * @return A XOM element containing image data.
	 */
	public static Element extractToXML(PdfReader reader){
    	Element root = new Element("Images");
    	PdfReaderContentParser parser = new PdfReaderContentParser(reader);
    	
    	// Go through the PDF one page at a time, pulling images from each page.
    	ImageRenderListener listener = new ImageRenderListener();
    	for (int i = 1; i <= reader.getNumberOfPages(); i++) {
    		try{
    			listener = parser.processContent(i, new ImageRenderListener());
    		}catch(IOException e){}
    		List<Element> images = listener.getImageData();
    		
    		// Add the current page number to each image, add it to the root.
    		if(images != null){
    			for(Element image : images){
    				image.addAttribute(new Attribute("Page", Integer.toString(i)));
    				root.appendChild(image);
    			}
    		}
    	}
    	
    	return root;
	}
	
	/**
	 * This class scans the page for images and returns a list of elements,
	 * one representing each image it finds.
	 */
    private static class ImageRenderListener implements RenderListener{

    	private List<Element> elements = new ArrayList<Element>();
    	
		@Override
		public void beginTextBlock() {
			
		}

		@Override
		public void endTextBlock() {
			
		}

		@Override
		public void renderImage(ImageRenderInfo renderInfo) {
			try{
				PdfNumber width = (PdfNumber)renderInfo.getImage().get(PdfName.WIDTH);
				PdfNumber height = (PdfNumber)renderInfo.getImage().get(PdfName.HEIGHT);
				//data = data + "<image width=\"" + width + "\" height=\"" + height + "\">\n</image>\n";
				Element element = new Element("Image");
				element.addAttribute(new Attribute("Width", width.toString()));
				element.addAttribute(new Attribute("Height", height.toString()));
				elements.add(element);
			}
			catch(Exception e){
				
			}
		}
		
		public List<Element> getImageData(){
			return elements;
		}

		@Override
		public void renderText(TextRenderInfo renderInfo) {
			
		}
    	
    }
}
