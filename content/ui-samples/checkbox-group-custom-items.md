<Path>Components > CheckboxGroup > CheckboxGroup with custom items</Path>

The list of CheckboxGroup items can be specified using the following methods: setItems() - allows you to specify programmatically component items; ComponentUtils.setItemsMap() - allows you to specify a string label for each item value explicitly;

checkbox-group-custom-items.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="flex-row flex-wrap">
        <checkboxGroup id="checkboxGroupWithList"
                       label="Items List"
                       themeNames="vertical"/>
        <checkboxGroup id="checkboxGroupWithMap"
                       label="Items Map"
                       themeNames="vertical"/>
        <checkboxGroup id="checkboxGroupWithEnum"
                       label="Items Enum"
                       themeNames="vertical"/>
    </layout>
</view>




CheckboxGroupCustomItemsSample.java

package io.jmix.uisamples.view.flowui.components.checkboxgroup.customitems;

import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.kit.component.ComponentUtils;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.CustomerGrade;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@ViewController("checkbox-group-custom-items")
@ViewDescriptor("checkbox-group-custom-items.xml")
public class CheckboxGroupCustomItemsSample extends StandardView {

    @ViewComponent
    protected JmixCheckboxGroup<Integer> checkboxGroupWithList;
    @ViewComponent
    protected JmixCheckboxGroup<Integer> checkboxGroupWithMap;
    @ViewComponent
    protected JmixCheckboxGroup<CustomerGrade> checkboxGroupWithEnum;

    @Subscribe
    protected void onInit(InitEvent event) {
        checkboxGroupWithList.setItems(getItemsList());
        ComponentUtils.setItemsMap(checkboxGroupWithMap, getItemsMap());
        checkboxGroupWithEnum.setItems(CustomerGrade.class);
    }

    protected List<Integer> getItemsList() {
        return List.of(2, 4, 5, 7);
    }

    protected Map<Integer, String> getItemsMap() {
        Map<Integer, String> itemsMap = new LinkedHashMap<>();
        itemsMap.put(2, "Two");
        itemsMap.put(4, "Four");
        itemsMap.put(5, "Five");
        itemsMap.put(7, "Seven");
        return itemsMap;
    }
}




CustomerGrade.java

package io.jmix.uisamples.entity;

import io.jmix.core.metamodel.datatype.EnumClass;
import org.springframework.lang.Nullable;

public enum CustomerGrade implements EnumClass<Integer> {

    PREMIUM(10),
    HIGH(20),
    STANDARD(30);

    private final Integer id;

    CustomerGrade(Integer id) {
        this.id = id;
    }

    @Override
    public Integer getId() {
        return id;
    }

    @Nullable
    public static CustomerGrade fromId(Integer id) {
        for (CustomerGrade grade : CustomerGrade.values()) {
            if (grade.getId().equals(id))
                return grade;
        }
        return null;
    }
}


