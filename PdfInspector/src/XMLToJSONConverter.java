import java.io.*;
public class XMLToJSONConverter {
	
	public static String drawJSONFromXML(String XMLFileName, String writeto)
	{
		// convert file to string
		String XMLString = "";
		try
		{
			String line;
			BufferedReader in = new BufferedReader(new FileReader(XMLFileName));
			while((line = in.readLine()) != null)
			{
				XMLString += line;
			}
		}catch(Exception e){System.err.println("XMLToJSONConverter error: " + e.getMessage());}	
		
		String tabLevel = "";
		String JSONString = "";
		String tag = "";
		String nameOfTag = "";
		String attributes = "";
		String text = "";
		
		int lnum = 0;
		
		while(!XMLString.equals(""))
		{
			lnum++;
			// if first character isn't '<' then must be text content
			if(XMLString.charAt(0) != '<')
			{
				text = XMLString.substring(0,XMLString.indexOf('<')); 
				// JSON doesn't like backslashes
				text = text.replaceAll("\\\\", "\\\\\\\\");
				JSONString += tabLevel + "{\n";
				JSONString += tabLevel + "\t\"text\":\"" + text + "\"\n";
				try{
					XMLString = XMLString.substring(XMLString.indexOf("<"));
				}catch(Exception e){}
				JSONString += tabLevel + "},\n";
			}
			// tag
			else
			{
				tag = XMLString.substring(0, XMLString.indexOf('>') + 1);
				
				try{
					if(tag.contains(" "))
						nameOfTag = tag.substring(1,tag.indexOf(' '));
					else
						nameOfTag = tag.substring(1,tag.indexOf('>'));
				}catch(Exception e){}
				
				// comment tag
				if(tag.contains("<!--"))
				{
					XMLString = XMLString.substring(XMLString.indexOf('>') + 1);
				}
				// prolog tag
				else if(tag.contains("<?"))
				{
					XMLString = XMLString.substring(XMLString.indexOf('>') + 1);
				}
				// end tag
				else if(tag.contains("</"))
				{
					XMLString = XMLString.substring(XMLString.indexOf('>') + 1);
					if(!JSONString.substring(JSONString.lastIndexOf(','),JSONString.length()).contains("content"))
						JSONString = JSONString.substring(0,JSONString.lastIndexOf(','));
					else JSONString = JSONString.trim();
					tabLevel = tabLevel.substring(1);
					JSONString += "\n" + tabLevel + "]\n";
					tabLevel = tabLevel.substring(1);
					JSONString += tabLevel + "},\n";
				}
				// start tag
				else
				{
					JSONString += tabLevel + "{\n";
					tabLevel += "\t";
					JSONString += tabLevel + "\"tagName\":\"" + nameOfTag + "\",\n";
					attributes = drawJSONAttributes(tabLevel, tag);
					if(!attributes.equals(""))
						JSONString += drawJSONAttributes(tabLevel, tag) + ",\n";
					JSONString += tabLevel + "\"content\":[\n";
					tabLevel += "\t";
					XMLString = XMLString.substring(XMLString.indexOf('>') + 1);
				}
			}
			
			XMLString = XMLString.trim();
		}
		
		JSONString = JSONString.substring(0,JSONString.lastIndexOf(','));
		
		try{
			if(writeto != null && writeto != ""){
				BufferedWriter out = new BufferedWriter(new FileWriter(writeto));
				out.write(JSONString);
				out.close();
			}
		}catch(Exception e){System.err.println("Error in XMLToJSONConverter function drawJSONFromXML():" + e.getMessage());}
		
		return JSONString;
	}
	
	// draws attributes of xml tag in form of json attributes
	// takes in a tag <blah att1=blah att2=blah>
	// returns
	// "attributes":[
	//   "att1":"blah",
	//   "att2":"blah"
	// ]
	public static String drawJSONAttributes(String tabLevel, String XMLString)
	{
		if(!XMLString.contains(" "))
			return tabLevel + "\"attributes\":[\n" + tabLevel + "]";
		XMLString = XMLString.substring(XMLString.indexOf(" ") + 1, XMLString.length() - 1);
		XMLString = XMLString.trim();
		
		if(XMLString.equals(""))
			return tabLevel + "\"attributes\":[\n" + tabLevel + "]";
		
		String JSONAttributes = tabLevel + "\"attributes\":[\n";
		String attribute = "";
		String value = "";
		while(!XMLString.equals(""))
		{
			attribute = XMLString.substring(0,XMLString.indexOf("="));
			XMLString = XMLString.substring(attribute.length() + 2);
			value = XMLString.substring(0,XMLString.indexOf("\""));
			XMLString = XMLString.substring(XMLString.indexOf("\"")+1);
			JSONAttributes += tabLevel + "\t" + "{\"" + attribute + "\"" + ":" + "\"" + value + "\"}" + ",\n";
			XMLString = XMLString.trim();
		}
		JSONAttributes = JSONAttributes.substring(0, JSONAttributes.lastIndexOf(','));
		JSONAttributes += "\n" + tabLevel + "]";
		
		return JSONAttributes;
	}
}
