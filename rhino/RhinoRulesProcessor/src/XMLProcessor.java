
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import java.io.*;
import java.util.*;

public class XMLProcessor {
	static String fileOut;
	static BufferedWriter out;
	static LinkedList<String> existingTags;
	static LinkedList<Integer> tagCount;

 public static void main(String argv[]) {
	 // create a list that will keep track of whether a tag already exists
	 existingTags = new LinkedList<String>();
	 tagCount = new LinkedList<Integer>();

  try {
  File file = new File("files/itext-rnua_manuallyedited.xml");
  DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
  DocumentBuilder db = dbf.newDocumentBuilder();
  Document doc = db.parse(file);
  
  Node root = doc.getDocumentElement();
  System.out.println("Root element " + root.getNodeName());
  
  fileOut = "files/TestWrite.txt";
  out = new BufferedWriter(new FileWriter(fileOut));
  String JSConversion = ParseXMLTree(root, uniqueName(root.getNodeName()));
  System.out.println(JSConversion);
  
  } catch (Exception e) {
    e.printStackTrace();
  }
 }
 
 public static String ParseXMLTree(Node node, String name) throws IOException{
	 String answer = "";
	 String cName = "";
	 String val = "";

	 val = node.getNodeValue();

	 System.out.println("name: " + name);
	 System.out.println("val: " + val + "\n");
	 answer += "var " + name + " = new Object();\n";
	 if(val != null)
	 {
		 val = val.replace('\n', ' ');
		 answer += name + ".value = \"" + val + "\";\n";
	 }
	 NodeList children = node.getChildNodes();
	 if(children.getLength() > 0)
	 {
		 answer += name + ".children = new Array();\n";
		 for(int j=0; j<children.getLength(); j++)
		 {
			 cName = children.item(j).getNodeName();
			 cName = uniqueName(cName);
			 answer += ParseXMLTree(children.item(j), cName);
			 answer += name + ".children[" + j + "] = " + cName + ";\n";
		 }
	 }
	 return answer;
 }
 
 static String uniqueName(String name)
 {
	 int tagInd;
	 Integer tagCnt;
	 
	 tagInd = existingTags.indexOf(name);
	 if(tagInd > -1)
	 {
		 tagCnt = tagCount.get(tagInd);
		 name += "_" + ++tagCnt;
		 tagCount.set(tagInd, tagCnt);
	 }
	 else
	 {
		 existingTags.add(name);
		 tagCount.add(new Integer(0));
		 name += "_" + 0;
	 }
	 
	 // clean name so that it is capable of being a variable name in JS
	 name = name.replaceAll("#", "");
	 name = name.replaceAll("-", "");
	 
	 return name;
 }
}