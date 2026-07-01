<Path>Components > TwinColumn > TwinColumn with custom items</Path>

The list of TwinColumn items can be specified using the following methods: setItems() - allows you to specify programmatically component items; ComponentUtils.setItemsMap() - allows you to specify a string label for each item value explicitly;

twin-column-custom-items.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="horizontal-layout">
        <twinColumn id="twinColumnWithList"
                    label="Items List"/>
        <twinColumn id="twinColumnWithMap"
                    label="Items Map"/>
        <twinColumn id="twinColumnWithEnum"
                    label="Items Enum"/>
    </layout>
</view>




TwinColumnCustomItemsSample.java

package io.jmix.uisamples.view.flowui.components.twincolumn.customitems;

import io.jmix.flowui.component.twincolumn.TwinColumn;
import io.jmix.flowui.kit.component.ComponentUtils;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.CustomerGrade;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@ViewController("twin-column-custom-items")
@ViewDescriptor("twin-column-custom-items.xml")
public class TwinColumnCustomItemsSample extends StandardView {

    @ViewComponent
    protected TwinColumn<Integer> twinColumnWithList;
    @ViewComponent
    protected TwinColumn<Integer> twinColumnWithMap;
    @ViewComponent
    protected TwinColumn<CustomerGrade> twinColumnWithEnum;

    @Subscribe
    protected void onInit(InitEvent event) {
        twinColumnWithList.setItems(getItemsList());
        ComponentUtils.setItemsMap(twinColumnWithMap, getItemsMap());
        twinColumnWithEnum.setItems(CustomerGrade.class);
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
import org.jspecify.annotations.Nullable;

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


