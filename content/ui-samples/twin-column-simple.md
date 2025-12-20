<Path>Components > TwinColumn > Simple TwinColumn</Path>

TwinColumn is a multiple selection component that shows two lists side by side, with the items column containing unselected items and the selectedItems column containing the selected items. Users can select the values by transferring them from the options to the select and backward using a double click or action buttons.

twin-column-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <hbox classNames="buttons-panel">
            <checkbox id="reorderableCheckbox" label="Reorderable"/>
            <checkbox id="selectAllButtonsCheckbox" label="Select all buttons visible"/>
        </hbox>
        <twinColumn id="twinColumn" label="Shopping list" itemsColumnLabel="Need to buy"
                    selectedItemsColumnLabel="Purchased"/>
    </layout>
</view>




TwinColumnSimpleSample.java

package io.jmix.uisamples.view.flowui.components.twincolumn.simple;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.component.twincolumn.TwinColumn;
import io.jmix.flowui.view.*;

@ViewController("twin-column-simple")
@ViewDescriptor("twin-column-simple.xml")
public class TwinColumnSimpleSample extends StandardView {

    @ViewComponent
    protected TwinColumn<String> twinColumn;

    @Subscribe
    public void onInit(InitEvent event) {
        twinColumn.setItems(
                "Whole Wheat Bread",
                "Chicken Breasts",
                "Brown Rice",
                "Milk",
                "Canned Black Beans",
                "Tomato Sauce",
                "Extra Virgin Olive Oil",
                "Bananas"
        );
    }

    @Subscribe("reorderableCheckbox")
    public void onReorderableCheckboxValueChange(ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        twinColumn.setReorderable(event.getValue());
    }

    @Subscribe("selectAllButtonsCheckbox")
    public void onSelectAllButtonsCheckboxValueChange(ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        twinColumn.setSelectAllButtonsVisible(event.getValue());
    }
}


