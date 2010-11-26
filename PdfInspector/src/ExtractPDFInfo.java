import java.io.*;
import java.util.HashMap;
import java.util.List;


public class ExtractPDFInfo {

    public static void main(String[] args) throws IOException {
    	
        try {
        	String filename = "testdocument-images";
        	String pathname = "C:/Users/Karen/Documents/Homework/PDF_Tests/pdfainspector/testcases/" +
        			filename + ".pdf";
        	String xmlFile = "C:/Users/Karen/Documents/Homework/PDF_Tests/pdfainspector/testcases/final-" +
			filename + ".xml";
        	
        	PdfExtractor extractor = new PdfExtractor(pathname);
        	
        	String tagFilename = "C:/Users/Karen/Documents/Homework/PDF_Tests/pdfainspector/testcases/itext-" +
				filename + ".xml";
            File tags = extractor.extractTags(tagFilename);
            
            String formFilename = "C:/Users/Karen/Documents/Homework/PDF_Tests/pdfainspector/testcases/form-" +
				filename + ".xml";
            File forms = extractor.extractForm(formFilename);
            
            String bookFilename ="C:/Users/Karen/Documents/Homework/PDF_Tests/pdfainspector/testcases/bookmarks-" +
				filename + ".xml";
            File bookmarks = extractor.extractBookmarks(bookFilename);
            
            PdfInfo info = new PdfInfo(tags, forms, bookmarks);
            info.exportAsXML(xmlFile);
            
            bookmarks.delete();
            forms.delete();
            
            XMLToJSON.convertXMLtoJSON(xmlFile, 
            		"C:/Users/Karen/Documents/Homework/PDF_Tests/pdfainspector/testcases/json-" +
    				filename + ".json");
        } catch (Exception e) {
        }
    }
    

}
