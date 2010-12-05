import java.io.File;


public class PdfAInspector {
	private static String pathname = "C:/Users/Kenneth/Desktop/Adobe PDF Repository/PdfInspector/files/";
	private static String filename = "tables-example2";
	
	public static void main(String[] args) {
		extractPdfInfo();
		RulesProcessor rprocessor = new RulesProcessor();
		rprocessor.runRules(pathname + "json-" + filename + ".js", pathname + "result_" + filename + ".js");
		
	}
	
	/**
	 * Extracts pdf info and returns as JSON in given pathname folder
	 */
    public static void extractPdfInfo() {
    	String pdfName = pathname + filename + ".pdf";
    	String xmlFile = pathname + "final-" + filename + ".xml";
    	
    	File forms, bookmarks, tags;
    	
    	PdfExtractor extractor = new PdfExtractor(pdfName);
    	
    	//extract information from PdfExtractor
    	//information extracted in separate try/catch blocks in order to ensure that they will all execute
    	
    	//extract tags
    	try{
    		String tagFilename = pathname + "itext-" +	filename + ".xml";
            tags = extractor.extractTags(tagFilename);
    	}
    	catch(Exception e)
    	{
    		System.out.println("Error in extracting tags");
    		tags = null;
    	}
    	
    	//extract forms
    	try{
    		String formFilename = pathname + "form-" +	filename + ".xml";
            forms = extractor.extractForm(formFilename);
    	}
    	catch(Exception e)
    	{
    		System.out.println("Error in extracting forms");
    		forms = null;
    	}
    	
    	//extract bookmarks
    	try{
    		String bookFilename = pathname + "bookmarks-" + filename + ".xml";
    		bookmarks = extractor.extractBookmarks(bookFilename);
    	}
    	catch(Exception e)
    	{
    		System.out.println("Error in extracting bookmarks");
    		bookmarks = null;
    	}
    	
    	
        PdfInfo info = new PdfInfo(tags, forms, bookmarks);
        info.exportAsXML(xmlFile);
            
        XMLToJSON.convertXMLtoJSON(xmlFile, pathname + "json-" + filename + ".js");
            
        //delete files
        if (bookmarks != null) bookmarks.delete();
        if (forms != null) forms.delete();
        if (tags != null) tags.delete();
        File xml = new File(xmlFile);
        xml.delete();
            
    }

   
}
