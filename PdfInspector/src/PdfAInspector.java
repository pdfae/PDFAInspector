import java.io.File;


public class PdfAInspector {
	private static String pathname = "C:/Users/Karen/Documents/Homework/PDF_Tests/pdfainspector/testcases/";
	private static String filename = "tables-example2";
	
	public static void main(String[] args) {
		extractPdfInfo();
		RulesProcessor rprocessor = new RulesProcessor();
		rprocessor.runRules(pathname + "json-" + filename + ".txt", pathname + "result_" + filename + ".txt");
		
	}
	
    public static void extractPdfInfo() {
    	
        try {
        	String pdfName = pathname + filename + ".pdf";
        	String xmlFile = pathname + "final-" + filename + ".xml";
        	
        	PdfExtractor extractor = new PdfExtractor(pdfName);
        	
        	String tagFilename = pathname + "itext-" +	filename + ".xml";
            File tags = extractor.extractTags(tagFilename);
            
            String formFilename = pathname + "form-" +	filename + ".xml";
            File forms = extractor.extractForm(formFilename);
            
            String bookFilename = pathname + "bookmarks-" + filename + ".xml";
            File bookmarks = extractor.extractBookmarks(bookFilename);
            
            PdfInfo info = new PdfInfo(tags, forms, bookmarks);
            info.exportAsXML(xmlFile);
            
            XMLToJSON.convertXMLtoJSON(xmlFile, 
            		pathname + "json-" + filename + ".txt");
            
            //delete files
            if (bookmarks != null) bookmarks.delete();
            if (forms != null) forms.delete();
            if (tags != null) tags.delete();
            
        } catch (Exception e) {
        }
    }
}
