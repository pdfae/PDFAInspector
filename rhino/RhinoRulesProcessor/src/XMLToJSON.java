import org.json.*;
import java.io.*;
import java.util.*;
public class XMLToJSON {

	public static void main(String[] args) {
	}
	
	public void convertXMLtoJSON(String XMLfile, String writeto)
	{
		// obj that will convert xml string to json obj
		XML converterObj = new XML();
		JSONObject jsonObj;
		
		// read in xml file
		String xml = "";
		try{
			String line;
			BufferedReader in = new BufferedReader(new FileReader(XMLfile));
			while((line = in.readLine()) != null)
			{
				xml += line + " ";
			}
			in.close();
		}catch(Exception e){System.err.println("reading xml file: " + e.getMessage());}
		
		// convert xml to json obj
		String root = "";
		try{
			jsonObj = converterObj.toJSONObject(xml);
			String[] roots = jsonObj.getNames(jsonObj);
			// read out json obj
			root = jsonObj.get(roots[0]).toString();			
		}catch(JSONException je){System.err.println("xml to json obj: " + je.getMessage());}
		
		try{
			BufferedWriter out = new BufferedWriter(new FileWriter(writeto));
			out.write(root);
			out.close();
		}catch(Exception e){System.err.println("write json obj to file: " + e.getMessage());}
	}
}
