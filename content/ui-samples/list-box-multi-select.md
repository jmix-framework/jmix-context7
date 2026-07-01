<Path>Components > ListBox > MultiSelectListBox</Path>

ListBox supports both single and multiple selection.

list-box-multi-select.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="horizontal-layout">
        <vbox width="AUTO">
            <h4 text="Single-select ListBox"/>
            <listBox id="listBox"/>
        </vbox>
        <vbox width="AUTO">
            <h4 text="Multi-select ListBox"/>
            <multiSelectListBox id="multiSelectListBox"/>
        </vbox>
    </layout>
</view>




ListBoxMultiSelectSample.java

package io.jmix.uisamples.view.flowui.components.listbox.multiselect;

import io.jmix.flowui.component.listbox.JmixListBox;
import io.jmix.flowui.component.listbox.JmixMultiSelectListBox;
import io.jmix.flowui.view.*;

import java.util.List;

@ViewController("list-box-multi-select")
@ViewDescriptor("list-box-multi-select.xml")
public class ListBoxMultiSelectSample extends StandardView {

    @ViewComponent
    protected JmixListBox<String> listBox;
    @ViewComponent
    protected JmixMultiSelectListBox<String> multiSelectListBox;

    @Subscribe
    protected void onInit(InitEvent event) {
        List<String> items = List.of("CSS", "HTML", "Java", "JavaScript", "JSON", "Kotlin", "XML");
        listBox.setItems(items);
        multiSelectListBox.setItems(items);

        listBox.setValue("Java");
        multiSelectListBox.select("Java", "Kotlin");
    }
}


