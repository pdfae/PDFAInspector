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
		}
       
		return null;
    }
    
    /**
     * Extract bookmarks and save as XML
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
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}

    }
    
    /**
     * extract metadata
     */
    public void extractMeta(){
        //extract metadata
        HashMap meta = reader.getInfo();
        String title = (String)meta.get("Title");
        String author = (String)meta.get("Author");
        String creator = (String)meta.get("Creator");
        String keywords = (String)meta.get("Keywords");
    }
    
    /**
     * Extract Permissions
     */
    public void extractPermissions(){
        System.out.println("File is opened with full permissions: " + reader.isOpenedWithFullPermissions());
    }
    
    /**
     * Extract Form Information
     */
    public File extractForm(String result){
        PrintWriter writer;
		try {
			File file = new File(result);
			writer = new PrintWriter(new FileOutputStream(file));
	    	AcroFields form = reader.getAcroFields();
	        // Loop over the fields and get field names
	    	
	        Set<String> fields = form.getFields().keySet();
	        String tag;
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
	        writer.flush();
	        writer.close();
	        
	        return file;
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}

    }
}
