import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;

/**
 * PDF data class holding information about tags, forms, and bookmarks
 * @author Karen
 */
public class PdfInfo {
	private File tagFile;
	private File formFile;
	private File bookmarkFile;
	private File metaFile;
	
	/**
	 * PdfInfo constructor
	 * @param tag : tag File
	 * @param form : forms File
	 * @param bookmark : bookmarks File
	 */
	public PdfInfo(File tag, File form, File bookmark, File meta){
		tagFile = tag;
		formFile = form;
		bookmarkFile = bookmark;
		metaFile = meta;
	}
	
	/**
	 * Copies the tag, form, and bookmark files into one file
	 * @param filename
	 * @return File
	 */
	public void exportAsXML(String outFilename){
		try {

			FileOutputStream output = new FileOutputStream(outFilename);
			PrintWriter writer = new PrintWriter(output);
			writer.println("<pdfinfo>");
			writer.flush();
			
			//metadata
			if (metaFile != null && metaFile.length() > 1){
				FileInputStream inputMeta = new FileInputStream(metaFile);
				copy(inputMeta, output);
			}
			
			//bookmarks
			if (bookmarkFile != null && bookmarkFile.length() > 1){
				FileInputStream inputBookmark = new FileInputStream(bookmarkFile);
				copy(inputBookmark, output);
			}
			else{
				writer.println("<bookmark></bookmark>");
				writer.flush();
			}
			//tags
			if (tagFile != null && tagFile.length() > 1){
				writer.println("<tags>");
				writer.flush();
				FileInputStream inputTag = new FileInputStream(tagFile);
				copy(inputTag, output);
				writer.println("</tags>");
				writer.flush();
			}
			else{
				writer.println("<tags></tags>");
				writer.flush();
			}
			//forms
			if (formFile != null && formFile.length() > 1){
				FileInputStream inputForm = new FileInputStream(formFile);
				copy(inputForm, output);
			}
			else{
				writer.println("<form></form>");
				writer.flush();
			}

			writer.println("</pdfinfo>");
			writer.flush();
			writer.close();
			
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
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
	
	/**
	 * Get tag file
	 * @return tagFile
	 */
	public File getTag(){
		return tagFile;
	}
	
	/**
	 * Set bookmark file
	 */
	public void setTag(File tg){
		tagFile = tg;
	}
	
	/**
	 * Get form file
	 * @return formFile
	 */
	public File getForm(){
		return formFile;
	}
	
	/**
	 * Set form file
	 */
	public void setForm(File fm){
		formFile = fm;
	}
	
	/**
	 * Get bookmark file
	 * @return bookmarkFile
	 */
	public File getBookmark(){
		return bookmarkFile;
	}
	
	/**
	 * Set bookmark file
	 */
	public void setBookmark(File bk){
		bookmarkFile = bk;
	}
	
}
