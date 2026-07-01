<Path>Components > ListBox > Simple ListBox</Path>

ListBox allows the user to select values from a scrollable list of items. ListBox is best suited for use as a lightweight, scrollable, single-column list for single or multi-selection of items. You can use separators to group related items.

list-box-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="horizontal-layout">
        <vbox width="AUTO">
            <h4 text="Simple ListBox"/>
            <listBox id="listBox"/>
        </vbox>
        <vbox width="AUTO">
            <h4 text="ListBox with separator"/>
            <listBox id="listBox2"/>
        </vbox>
    </layout>
</view>




ListBoxSimpleSample.java

package io.jmix.uisamples.view.flowui.components.listbox.simple;

import com.vaadin.flow.component.html.Hr;
import io.jmix.flowui.component.listbox.JmixListBox;
import io.jmix.flowui.view.*;

import java.util.List;

@ViewController("list-box-simple")
@ViewDescriptor("list-box-simple.xml")
public class ListBoxSimpleSample extends StandardView {

    @ViewComponent
    protected JmixListBox<String> listBox;
    @ViewComponent
    protected JmixListBox<String> listBox2;

    @Subscribe
    protected void onInit(InitEvent event) {
        List<String> items = List.of("Jmix", "Vaadin", "SpringBoot", "EclipseLink");
        listBox.setItems(items);
        listBox2.setItems(items);

        listBox.setValue("Jmix");
        listBox2.setValue("Jmix");

        listBox2.addComponents("Vaadin", new Hr());
    }
}


