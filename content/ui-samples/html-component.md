<Path>Components > HTML > HTML Component</Path>

To display native HTML content, use the Html component. The Html component can be added programmatically or declaratively. Please note that the HTML content must have only one root tag (for example, div).

html-component.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <tabSheet id="tabSheet" width="100%">
            <tab id="declarativeTab" label="Declaratively added component">
                <html file="META-INF/resources/html/html-component.html"/>
            </tab>
        </tabSheet>
    </layout>
</view>




HtmlComponentSample.java

package io.jmix.uisamples.view.flowui.components.html.htmlcomponent;

import com.vaadin.flow.component.Html;
import io.jmix.core.Resources;
import io.jmix.flowui.component.tabsheet.JmixTabSheet;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.io.InputStream;

@ViewController("html-component")
@ViewDescriptor("html-component.xml")
public class HtmlComponentSample extends StandardView {

    protected static final String SRC_PATH = "META-INF/resources/html/html-component.html";

    @ViewComponent
    protected JmixTabSheet tabSheet;

    @Autowired
    protected Resources resources;

    @Subscribe
    protected void onInit(InitEvent event) {
        InputStream resourceAsStream = resources.getResourceAsStream(SRC_PATH);

        Html html = new Html(resourceAsStream);
        tabSheet.add("Programmatically added component", html);
    }
}




html-component.html

<div>
    <h1>HTML Tags Sample</h1>

    <p>This is a sample text that showcases the usage of different HTML tags.</p>

    <h2>Formatting Tags:</h2>
    <p>Here are some formatting tags:</p>
    <ul>
        <li><b>Bold text:</b> Use the &lt;b&gt; tag to make text <b>bold</b>.</li>
        <li><i>Italic text:</i> Use the &lt;i&gt; tag to make text <i>italic</i>.</li>
        <li><span class="highlight">Highlighted text:</span> Use the &lt;span&gt; tag to add a
            <span class="highlight">highlighted effect</span> to text.</li>
    </ul>

    <h2>Lists:</h2>
    <p>Here are some examples of lists:</p>
    <h3>Ordered List:</h3>
    <ol>
        <li>First item</li>
        <li>Second item</li>
        <li>Third item</li>
    </ol>

    <h3>Unordered List:</h3>
    <ul>
        <li>Apples</li>
        <li>Oranges</li>
        <li>Bananas</li>
    </ul>

    <h2>Hyperlinks:</h2>
    <p>Hyperlinks can be added using the &lt;a&gt; tag:</p>
    <a href="https://www.jmix.io" target="_blank">Visit jmix.io</a>

</div>



html-component.css


.highlight {
    color: red;
    font-weight: bold;
}

.font-italic {
    font-style: italic;
}

