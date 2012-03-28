package pdfainspector;

import java.util.Set;

import nu.xom.Element;

import com.itextpdf.text.pdf.PdfDictionary;
import com.itextpdf.text.pdf.PdfName;
import com.itextpdf.text.pdf.PdfReader;

public class RoleMapExtractor {

	/**
	 * Given an iText PDF Reader, extract the role map from the PDF and store
	 * it in a XOM XML element.
	 * @param reader A reader for the given PDF.
	 * @return A XOM element containing tag data.
	 */
	public static Element extractToXML(PdfReader reader){
		Element root = new Element("RoleMap");
		PdfDictionary catalog = reader.getCatalog();
		if(!catalog.contains(PdfName.STRUCTTREEROOT)){
			return root;
		}
		PdfDictionary structTree = catalog.getAsDict(PdfName.STRUCTTREEROOT);
		if(!structTree.contains(PdfName.ROLEMAP)){
			return root;
		}
		PdfDictionary roleMap = structTree.getAsDict(PdfName.ROLEMAP);
		Set<PdfName> keys = roleMap.getKeys();
		for(PdfName key : keys){
			Element mapElement = new Element(fixTagName(PdfName.decodeName(key.toString())));
			mapElement.appendChild(fixTagName(PdfName.decodeName(roleMap.getAsName(key).toString())));
			root.appendChild(mapElement);
		}
		return root;
	}
	
    /**
     * Taken from iText's TaggedPdfReaderTool, this renders tag names into an
     * XML-compatible format.
     * @param tag The tag to format.
     * @return A string representing the tag name.
     */
    private static String fixTagName(String tag) {
        StringBuilder sb = new StringBuilder();
        for (int k = 0; k < tag.length(); ++k) {
            char c = tag.charAt(k);
            boolean nameStart =
                c == ':'
                || (c >= 'A' && c <= 'Z')
                || c == '_'
                || (c >= 'a' && c <= 'z')
                || (c >= '\u00c0' && c <= '\u00d6')
                || (c >= '\u00d8' && c <= '\u00f6')
                || (c >= '\u00f8' && c <= '\u02ff')
                || (c >= '\u0370' && c <= '\u037d')
                || (c >= '\u037f' && c <= '\u1fff')
                || (c >= '\u200c' && c <= '\u200d')
                || (c >= '\u2070' && c <= '\u218f')
                || (c >= '\u2c00' && c <= '\u2fef')
                || (c >= '\u3001' && c <= '\ud7ff')
                || (c >= '\uf900' && c <= '\ufdcf')
                || (c >= '\ufdf0' && c <= '\ufffd');
            boolean nameMiddle =
                c == '-'
                || c == '.'
                || (c >= '0' && c <= '9')
                || c == '\u00b7'
                || (c >= '\u0300' && c <= '\u036f')
                || (c >= '\u203f' && c <= '\u2040')
                || nameStart;
            if (k == 0) {
                if (!nameStart)
                    c = '_';
            }
            else {
                if (!nameMiddle)
                    c = '-';
            }
            sb.append(c);
        }
        return sb.toString();
    }
}
