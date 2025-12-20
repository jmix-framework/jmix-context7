<Path>Components > RadioButtonGroup > RadioButtonGroup with custom items</Path>

The list of RadioButtonGroup items can be specified using the following methods: setItems() - allows you to specify programmatically component items; ComponentUtils.setItemsMap() - allows you to specify a string label for each item value explicitly;

radio-button-group-custom-items.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="flex-row flex-wrap">
        <radioButtonGroup id="radioButtonGroupWithList"
                          label="Items List"
                          themeNames="vertical"/>
        <radioButtonGroup id="radioButtonGroupWithMap"
                          label="Items Map"
                          themeNames="vertical"/>
        <radioButtonGroup id="radioButtonGroupWithEnum"
                          label="Items Enum"
                          themeNames="vertical"/>
    </layout>
</view>




RadioButtonGroupCustomItemsSample.java

package io.jmix.uisamples.view.flowui.components.radiobuttongroup.customitems;

import io.jmix.flowui.component.radiobuttongroup.JmixRadioButtonGroup;
import io.jmix.flowui.kit.component.ComponentUtils;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.CustomerGrade;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@ViewController("radio-button-group-custom-items")
@ViewDescriptor("radio-button-group-custom-items.xml")
public class RadioButtonGroupCustomItemsSample extends StandardView {

    @ViewComponent
    protected JmixRadioButtonGroup<Integer> radioButtonGroupWithList;
    @ViewComponent
    protected JmixRadioButtonGroup<Integer> radioButtonGroupWithMap;
    @ViewComponent
    protected JmixRadioButtonGroup<CustomerGrade> radioButtonGroupWithEnum;

    @Subscribe
    protected void onInit(InitEvent event) {
        radioButtonGroupWithList.setItems(getItemsList());
        ComponentUtils.setItemsMap(radioButtonGroupWithMap, getItemsMap());
        radioButtonGroupWithEnum.setItems(CustomerGrade.class);
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


