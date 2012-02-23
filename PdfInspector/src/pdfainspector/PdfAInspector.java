package pdfainspector;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintWriter;

/**
 * Executable file of PdfInspector.
 * This is the main class, which calls the XML and JSON generators and feeds
 * the results to the Rules Engine.
 * @author schiele1
 */
public class PdfAInspector {
	
	/**
	 * Reads in the PDF files, calls the XML and JSON generators in the
	 * PdfExtractor class, and feeds the results to the Rules Engine.
	 * @param args A list of space-separated strings, each being the filepath
	 * to a PDF on which the inspector is to be run.
	 */
	public static void main(String[] args){
		// Make sure there's actually a file to inspect.
		if(args.length == 0 || args[0].equals("-h") || args[0].equals("-help")){
			System.out.println("Usage: java -jar pdfainspector.jar \"/path/to/file/document.pdf\"\n" +
					"You can simultaneously enter any number of filepaths, separated by spaces," +
					" all enclosed in quotes (if they have spaces) and all of them will be analyzed.\n" +
					"You can type java -jar pdfainspector.jar -h or -help to display this help message.");
			return;
		}
		
		// Run our rules on each specified PDF, but only if it's a PDF.
		for(String pdfName : args){
			if(!checkExtension(pdfName)){
				System.err.println(pdfName + " is not a PDF File");
				continue;
			}
			
			// Determine the source PDF and destination XML and JSON files.
			String pathname = extractPath(pdfName);
			String filename = extractFilename(pdfName);
			String xmlName = pathname + "xml-" + filename + ".xml";
			String jsonName = pathname + "json-" + filename + ".json";
			PrintWriter writer;
			
			// Generate our XML file using the PdfExtractor class.
			System.out.println("Generating XML for " + pdfName + "...");
			File xmlFile = new File(xmlName);
			String xml = PdfExtractor.extractToXML(pdfName);
			try{
				writer = new PrintWriter(new FileOutputStream(xmlFile));
				writer.println(xml);
				writer.flush();
				writer.close();
			}catch(FileNotFoundException e){
				System.err.println("Error generating XML file for " + pdfName);
				return;
			}
			System.out.println("XML file " + xmlName + " generated.");
			
			// Convert our XML file to JSON using PdfExtractor.
			System.out.println("Generating JSON for " + pdfName + "...");
			File jsonFile = new File(jsonName);
			String json = PdfExtractor.convertXMLToJSON(xml);
			try{
				writer = new PrintWriter(new FileOutputStream(jsonFile));
				writer.println(json);
				writer.flush();
				writer.close();
			}catch(FileNotFoundException e){
				System.err.println("Error generating JSON file for " + pdfName);
				return;
			}
			System.out.println("JSON file " + jsonName + " generated.");
		}
	}
	
	/**
	 * Given a filepath, it separates the path from the filename and returns
	 * the path.
	 * @param filepath The filepath string from which to extract.
	 * @return The path component of the string, without the filename or
	 * extension.
	 */
	public static String extractPath(String filepath){
		int lastSlash = filepath.lastIndexOf('/');
		if(lastSlash >= 0){
			return filepath.substring(0, lastSlash + 1);
		}
		return "";
	}
	
	/**
	 * Given a filepath, it separates the path from the filename and returns
	 * the filename, without the extension.
	 * @param filepath The filepath string from which to extract.
	 * @return The filename component of the string, without the path or
	 * extension.
	 */
	public static String extractFilename(String filepath){
		int lastDot = filepath.lastIndexOf('.');
		int lastSlash = filepath.lastIndexOf('/');
		return filepath.substring(lastSlash + 1, lastDot);
	}
	
	/**
	 * Checks whether the extension of the given filepath is pdf.
	 * @param filepath The filepath to check.
	 * @return True if the extension is .pdf, False if it isn't.
	 */
	public static boolean checkExtension(String filepath){
		int lastDot = filepath.lastIndexOf('.');
		if(lastDot >= 0){
			String extension = filepath.substring(lastDot + 1);
			return extension.toLowerCase().equals("pdf");
		}
		return false;
	}
}
