import java.io.File;
import java.io.IOException;

/**
 * Executable file of PdfInspector
 * Extracts pdf info, converts it to json, then runs rules on it
 * @param complete pathname of pdf file to be evaluated
 *
 */
public class PdfAInspector {
	private static String pathname;
	private static String filename;
	private static String jsonFilename;
	
	public static void main(String[] args) {
		
		pathname = extractPath(args[0]);
		filename = extractFilename(args[0]);
		
		jsonFilename = pathname + "json-" + filename + ".json";
		
		System.out.println("extracting PDF info on \"" + filename + "\"...");
		extractPdfInfo();
		System.out.println("finished extracting PDF info!");
		RulesProcessor rprocessor = new RulesProcessor();
		System.out.println("running rules on PDF...");
		rprocessor.runRules(jsonFilename, pathname, "result_" + filename + ".json");
		System.out.println("finished running rules on PDF!");
		System.out.println("file written to: " + pathname);
		System.out.println("file is called: " + "result_" + filename + ".json");

		//delete json file
        //File jsonFile = new File(jsonFilename);
        //jsonFile.delete();
	}
	
	/**
	 * Extracts pdf info and returns as JSON in given pathname folder
	 */
    public static void extractPdfInfo() {
    	String pdfName = pathname + filename + ".pdf";
    	String xmlFile = pathname + "final-" + filename + ".xml";
    	
    	File forms = null, bookmarks = null, tags = null, meta = null;
    	
    	PdfExtractor extractor = new PdfExtractor(pdfName);
    	
    	//extract information from PdfExtractor
    	//information extracted in separate try/catch blocks in order to ensure that they will all execute
    	
    	//extract metadata
    	try{
    		String metaFilename = pathname + "meta-" +	filename + ".xml";
            meta = extractor.extractMeta(metaFilename);
    	}
    	catch(Exception e)
    	{
    		System.out.println("Error in extracting metadata");
    		if (meta != null){
    			meta.delete();
    			meta = null;
    		}
    	}
    	
    	//extract tags
    	try{
    		String tagFilename = pathname + "itext-" +	filename + ".xml";
    		String outlineFilename = pathname + filename + "_outline.xml";
            tags = extractor.extractTags(tagFilename, outlineFilename);
            //tags = extractor.convertToXmlWithAttr(tagFilename);
    	}
    	catch(Exception e)
    	{
    		System.out.println("Error in extracting tags");
    		if (tags != null){
    			tags.delete();
        		tags = null;
    		}
    	}
    	
    	//extract forms
    	try{
    		String formFilename = pathname + "form-" +	filename + ".xml";
            forms = extractor.extractForm(formFilename);
    	}
    	catch(Exception e)
    	{
    		System.out.println("Error in extracting forms");
    		if (forms != null){
    			forms.delete();
    			forms = null;
    		}	
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
    	
        PdfInfo info = new PdfInfo(tags, forms, bookmarks, meta);
        try {
			info.exportAsXML(xmlFile);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
        
        //XMLToJSON.convertXMLtoJSON(xmlFile, jsonFilename);
        XMLToJSONConverter.drawJSONFromXML(xmlFile, jsonFilename);
        
        //delete files
        if (meta != null) meta.delete();
        if (bookmarks != null) bookmarks.delete();
        if (forms != null) forms.delete();
        if (tags != null) tags.delete();

    }
    
    /**
     * Extracts the pathname of a string
     */
    public static String extractPath(String str){
    	for (int x = str.length()-1; x>0; x--){
    		if (str.charAt(x) == '/'){
    			return str.substring(0, x+1);
    		}
    	}
    	return null;
    }
    
    /**
     * Extracts the filename of a string
     */
    public static String extractFilename(String str){
    	int extensionPos = str.length()-1;
    	
    	for (int x = str.length()-1; x>0; x--){
    		if (str.charAt(x) == '.'){
    			extensionPos = x;
    		}
    		if (str.charAt(x) == '/'){
    			return str.substring(x+1,extensionPos);
    		}
    		
    	}
    	return null;    	
    }
}