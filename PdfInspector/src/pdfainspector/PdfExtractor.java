package pdfainspector;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

import nu.xom.Document;
import nu.xom.Element;
import nu.xom.Serializer;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONML;
import org.json.JSONObject;

import com.itextpdf.text.pdf.PdfReader;

/**
 * Given the path to a PDF file, PdfExtractor generates an XML tree of its
 * accessibility components. Given such an XML file, it converts that tree to
 * JSON for rules processing.
 * @author schiele1
 */
public class PdfExtractor {
	
	/**
	 * Scans the PDF for several indicators of accessibility (metadata,
	 * bookmarks, tags, form data, text, and image data), and writes them to
	 * an XML string.
	 * @param pdfName The path to the PDF file to be inspected.
	 * @return A string containing the XML tree representing the PDF.
	 */
	public static String extractToXML(String pdfName){
		// Initialize the reader which will scan the PDF for our data.
		PdfReader reader = null;
		try{
			reader = new PdfReader(pdfName);
		}catch(IOException e){
			return null;
		}
		
		// Use our reader to scan the PDF for each of the necessary components.
		Element root = new Element("PdfInfo");
		Element meta = MetaExtractor.extractToXML(reader);
		Element bookmarks = BookmarkExtractor.extractToXML(reader);
		Element tags = TagExtractor.extractToXML(reader);
		Element form = FormExtractor.extractToXML(reader);
		//Element text = TextExtractor.extractToXML(reader);
		//Element images = ImageExtractor.extractToXML(reader);
		
		// Add each component to the root of our XML tree.
		root.appendChild(meta);
		root.appendChild(bookmarks);
		root.appendChild(tags);
		root.appendChild(form);
		//root.appendChild(text);
		//root.appendChild(images);
		
		// Format and return the now-complete tree.
		Document doc = new Document(root);
		ByteArrayOutputStream baos = new ByteArrayOutputStream();
		try{		
			Serializer serializer = new Serializer(baos);
			serializer.setIndent(4);
			serializer.write(doc);
		}catch(Exception e){
			System.err.println("Error extracting XML");
		}
		return baos.toString();
	}
	
	/**
	 * Given an XML string, presumably representing a PDF, convert that file
	 * into a JSON string, specially formatted for rules parsing.
	 * @param xml The XML string to be converted.
	 * @return The formatted JSON string.
	 */
	public static String convertXMLToJSON(String xml){
		String json = "";
		try {
			JSONObject j = JSONML.toJSONObject(xml);
			j = formatJSON(j);
			json = j.toString(4);
		} catch (JSONException e) {
			System.err.println("Error converting to JSON");
		}
		return json;
	}
	
	/**
	 * A helper function for our JSON converter, formatJSON rearranges the JSON
	 * objects into an order better suited for reading by our rules engine.
	 * @param j The JSON object to be formatted.
	 * @return The formatted JSON object.
	 * @throws JSONException
	 */
	private static JSONObject formatJSON(JSONObject j) throws JSONException{
		JSONArray children = new JSONArray();
		JSONArray attributes = new JSONArray();
		String[] names = JSONObject.getNames(j);
		
		for(String name : names){
			Object obj = j.get(name);
			
			// Recursively format each child object.
			if(name.equals("childNodes") && obj instanceof JSONArray){
				children = (JSONArray)j.remove("childNodes");
				for(int i = 0; i < children.length(); i ++){
					Object childObj = children.get(i);
					if(childObj instanceof JSONObject){
						formatJSON((JSONObject)childObj);
					}
				}
			}
			
			// Add any attributes to the attribute array.
			else if(!name.equals("tagName")){
				JSONObject child = new JSONObject();
				child.put(name, obj);
				attributes.put(child);
				j.remove(name);
			}
		}
		
		j.put("attributes", attributes);
		j.put("content", children);
		return j;
	}

}
