package pdfainspector;
import java.util.Set;

import nu.xom.Element;

import com.itextpdf.text.pdf.AcroFields;
import com.itextpdf.text.pdf.PdfDictionary;
import com.itextpdf.text.pdf.PdfName;
import com.itextpdf.text.pdf.PdfReader;

/**
 * Convert form data in a PDF to a XOM XML element.
 * @author schiele1
 */
public class FormExtractor {

	/**
	 * Given an iText PDF Reader, extract form data from the PDF and store it
	 * in a XOM XML element.
	 * @param reader A reader for the given PDF.
	 * @return A XOM element containing form data.
	 */
	public static Element extractToXML(PdfReader reader){
		Element root = new Element("Form");
    	AcroFields form = reader.getAcroFields();
        Set<String> fields = form.getFields().keySet();
        
        String tag;
        // Determine the field type each form object represents.
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
	            	tag = "unknown";
            }
            
            // Create the element corresponding to each tag.
            Element tagElement = new Element(tag);
            Element name = new Element("Name");
            name.appendChild(key);
            tagElement.appendChild(name);
            
            // Give the element its attributes (tooltips) and add it to root.
            int numWidgets = form.getFieldItem(key).size();
            for (int j = 0; j < numWidgets; j++){
            	PdfDictionary widget = form.getFieldItem(key).getWidget(j);
            	if (widget.get(PdfName.TU) != null){
            		Element tooltip = new Element("Tooltip");
	            		tooltip.appendChild(widget.get(PdfName.TU).toString());
	            		tagElement.appendChild(tooltip);
	            	}
	            }
	            root.appendChild(tagElement);
	        }
 
	        
	        return root;
	}
}
