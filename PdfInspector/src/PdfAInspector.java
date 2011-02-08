import java.io.File;

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
		
		extractPdfInfo();
		RulesProcessor rprocessor = new RulesProcessor();
		rprocessor.runRules(jsonFilename, pathname + "Tempfiles/results/" + "result_" + filename + ".json");

		//delete json file
        File jsonFile = new File(jsonFilename);
        jsonFile.delete();
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
    		meta.delete();
    		meta = null;
    	}
    	
    	//extract tags
    	try{
    		String tagFilename = pathname + "itext-" +	filename + ".xml";
            tags = extractor.extractTags(tagFilename);
    	}
    	catch(Exception e)
    	{
    		System.out.println("Error in extracting tags");
    		tags.delete();
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
    		forms.delete();
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
    	
    	
        PdfInfo info = new PdfInfo(tags, forms, bookmarks, meta);
        info.exportAsXML(xmlFile);
        
        
        XMLToJSON.convertXMLtoJSON(xmlFile, jsonFilename);
            
        //delete files
        if (meta != null) meta.delete();
        if (bookmarks != null) bookmarks.delete();
        if (forms != null) forms.delete();
        if (tags != null) tags.delete();
        File xml = new File(xmlFile);
        xml.delete();

            
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
