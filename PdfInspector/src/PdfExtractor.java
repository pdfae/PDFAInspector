import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.List;
import java.util.Set;

import com.itextpdf.text.pdf.AcroFields;
import com.itextpdf.text.pdf.PdfDictionary;
import com.itextpdf.text.pdf.PdfName;
import com.itextpdf.text.pdf.PdfReader;
import com.itextpdf.text.pdf.SimpleBookmark;
import com.itextpdf.text.pdf.parser.TaggedPdfReaderTool;

/**
 * PdfExtractor
 * Extracts information and saves it to a separate xml file, determined by the filename parameter
 * Currently extracts: tags, form information, metadata, and bookmarks
 * @author Karen
 */
public class PdfExtractor {
	private String filename;
	private PdfReader reader;
	
	
	public PdfExtractor(String filename){
		this.filename = filename;
		try {
			reader = new PdfReader(this.filename);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
    /**
     * Extract tags and save as XML
     * @return tags as an xml File
     * @throws IOException 
     */
    public File extractTags(String result) throws IOException{
		try {
			TaggedPdfReaderTool tReader = new TaggedPdfReaderTool();
			FileOutputStream fop;
			File file = new File(result);
			fop = new FileOutputStream(file);
			tReader.convertToXml(reader, fop);
		        
		    fop.flush();
		    fop.close();
		    
		    return file;
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}
       

    }
    
    /**
     * Extract bookmarks and save as XML
     * @return bookmark information as a xml file
     */
    public File extractBookmarks(String result){
		try {
			File file = new File(result);
			FileOutputStream fop = new FileOutputStream(file);
	        List<HashMap<String,Object>> list = SimpleBookmark.getBookmark(reader);
	        if (list == null) return null;
	        SimpleBookmark.exportToXML(list, fop, "ISO8859-1", true);
	        return file;
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}

    }
    
    /**
     * extract metadata
     * @return metadata information as xml file
     */
    public File extractMeta(String filename){
    	try{
    		File file = new File(filename);
    		PrintWriter writer = new PrintWriter(new FileOutputStream(file));
    	
        	//extract metadata
        	HashMap meta = reader.getInfo();
        	String title = (String)meta.get("Title");
        	String author = (String)meta.get("Author");
        	String creator = (String)meta.get("Creator");
        	String keywords = (String)meta.get("Keywords");
        
        	writer.println("<title>");
        	writer.println(title);
        	writer.println("</title>");
        	
        	writer.println("<author>");
        	writer.println(author);
        	writer.println("</author>");
        	
        	writer.println("<creator>");
        	writer.println(creator);
        	writer.println("</creator>");
        	
        	writer.println("<keywords>");
        	writer.println(keywords);
        	writer.println("</keywords>");
        
        	writer.flush();
        	writer.close();
        	
        	return file;
    	}
    	catch(Exception e){
    		e.printStackTrace();
    		return null;
    	}
    }
    
    /**
     * Extract Permissions
     * Currently unused; returns a boolean whether it is opened w/ full permissions
	 * @return isOpenedWithFullPermissions
     */
    public boolean extractPermissions(){
        return reader.isOpenedWithFullPermissions();
    }
    
    /**
     * Extract Form Information and writes into an xml file determined by the param result
     * @param result : output xml file
     * @return form information as a xml file
     */
    public File extractForm(String result){
        PrintWriter writer;
		try {
			File file = new File(result);
			writer = new PrintWriter(new FileOutputStream(file));
	    	AcroFields form = reader.getAcroFields();
	        
	    	writer.println("<form>");
	    	// Loop over the fields and get field names
	    	
	        Set<String> fields = form.getFields().keySet();
	        String tag;
	        // determines what form field it is
	        for (String key : fields){
	            switch (form.getFieldType(key)) {
	            case AcroFields.FIELD_TYPE_CHECKBOX:
	            	tag = "Checkbox";
	                break;
	            case AcroFields.FIELD_TYPE_COMBO:
	            	tag = "Combobox";
	                break;
	            case AcroFields.FIELD_TYPE_LIST:
	            	tag = "List";
	                break;
	            case AcroFields.FIELD_TYPE_NONE:
	            	tag = "None";
	                break;
	            case AcroFields.FIELD_TYPE_PUSHBUTTON:
	            	tag = "Pushbutton";
	                break;
	            case AcroFields.FIELD_TYPE_RADIOBUTTON:
	            	tag = "Radiobutton";
	                break;
	            case AcroFields.FIELD_TYPE_SIGNATURE:
	            	tag = "Signature";
	                break;
	            case AcroFields.FIELD_TYPE_TEXT:
	            	tag = "Text";
	                break;
	            default:
	                //if unknown
	            	tag = "unknown";
	            }
	            writer.println("<" + tag + ">");
	            writer.println('\t' + "<Name>" + key + "</Name>");
	            
	            int numWidgets = form.getFieldItem(key).size();
	            for (int j = 0; j < numWidgets; j++){
	            	PdfDictionary widget = form.getFieldItem(key).getWidget(j);
	            	if (widget.get(PdfName.TU) != null)
	            		writer.println('\t' + "<Tooltip>" + widget.get(PdfName.TU) + "</Tooltip>");
	            }
	            
	            writer.println("</" +tag+ ">");
	        }
	        writer.println("</form>");
	        writer.flush();
	        writer.close();
	        
	        return file;
		} catch (FileNotFoundException e) {
			e.printStackTrace();
			return null;
		}

    }
}
