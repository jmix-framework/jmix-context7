<Path>Components > MultiSelectComboBox > Simple MultiSelectComboBox</Path>

multiSelectComboBox allows users to choose one or more items from a drop-down list. clearButtonVisible attribute allows users to clear all selected items. multiSelectComboBox supports the following features from the regular comboBox: Custom items Custom filtering Handling user input Custom renderer

multi-select-combo-box-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="horizontal-layout">
        <multiSelectComboBox id="multiSelectComboBox"/>
        <multiSelectComboBox itemsEnum="io.jmix.uisamples.entity.Day" clearButtonVisible="true" width="17em"/>
    </layout>
</view>




MultiSelectComboBoxSimpleSample.java

package io.jmix.uisamples.view.flowui.components.multiselectcombobox.simple;

import io.jmix.flowui.component.multiselectcombobox.JmixMultiSelectComboBox;
import io.jmix.flowui.view.*;

@ViewController("multi-select-combo-box-simple")
@ViewDescriptor("multi-select-combo-box-simple.xml")
public class MultiSelectComboBoxSimpleSample extends StandardView {

    @ViewComponent
    protected JmixMultiSelectComboBox<String> multiSelectComboBox;

    @Subscribe
    protected void onInit(InitEvent event) {
        multiSelectComboBox.setItems("CSS", "HTML", "Java", "JavaScript", "JSON", "Kotlin", "XML");
        multiSelectComboBox.select("Java", "Kotlin");
    }
}




Day.java

package io.jmix.uisamples.entity;

import io.jmix.core.metamodel.datatype.EnumClass;
import org.jspecify.annotations.Nullable;

public enum Day implements EnumClass<String> {

    SUNDAY("sun"),
    MONDAY("mon"),
    TUESDAY("tue"),
    WEDNESDAY("wed"),
    THURSDAY("thu"),
    FRIDAY("fri"),
    SATURDAY("sat");

    private final String id;

    Day(String value) {
        this.id = value;
    }

    @Override
    public String getId() {
        return id;
    }

    @Nullable
    public static Day fromId(String id) {
        for (Day day : Day.values()) {
            if (day.getId().equals(id)) {
                return day;
            }
        }
        return null;
    }
}

