import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;

/**
 * PDF data class
 * @author Karen
 *
 */
public class PdfInfo {
	private File tagFile;
	private File formFile;
	private File bookmarkFile;
	
	public PdfInfo(File tag, File form, File bookmark){
		tagFile = tag;
		formFile = form;
		bookmarkFile = bookmark;
	}
	
	/**
	 * Copies the tag, form, and bookmark files into one file
	 * @param filename
	 * @return File
	 */
	public File exportAsXML(String filename){
		try {

			FileOutputStream output = new FileOutputStream(filename);
			PrintWriter writer = new PrintWriter(output);
			writer.println("<pdfinfo>");
			writer.flush();
			
			//bookmarks
			if (bookmarkFile == null || bookmarkFile.length() > 1){
				FileInputStream inputBookmark = new FileInputStream(bookmarkFile);
				copy(inputBookmark, output);
			}
			else{
				writer.println("<bookmark></bookmark>");
				writer.flush();
			}
			//tags
			if (tagFile.length() > 1){
				writer.println("<tag>");
				writer.flush();
				FileInputStream inputTag = new FileInputStream(tagFile);
				copy(inputTag, output);
				writer.println("</tag>");
				writer.flush();
			}
			else{
				writer.println("<tag></tag>");
				writer.flush();
			}
			//forms
			if (formFile.length() > 1){
				FileInputStream inputForm = new FileInputStream(formFile);
				copy(inputForm, output);
			}
			else{
				writer.println("<form></form>");
				writer.flush();
			}

			writer.println("</pdfinfo>");
			writer.close();
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return new File(filename);
	}
	
	/**
	 * Copies input file into output file
	 * @param in
	 * @param out
	 */
	private void copy(InputStream in, OutputStream out){
		try{
			byte[] buf = new byte[1024];
			int len;
			while ((len = in.read(buf)) > 0){
				out.write(buf, 0, len);
			}	
			in.close();
			}
		catch(Exception e){
			
		}
	}
	
	public File getTag(){
		return tagFile;
	}
	
	public File getForm(){
		return formFile;
	}
	
	public File getBookmark(){
		return bookmarkFile;
	}

}
