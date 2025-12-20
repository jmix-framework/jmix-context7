<Path>Components > CheckboxGroup > Simple CheckboxGroup</Path>

CheckboxGroup allows a user to select multiple values from a list of options using checkboxes. The themeNames attribute defines the orientation of group elements. By default, elements are arranged horizontally. In this example, CheckboxGroup is used to select an enumeration value for an entity attribute.

checkbox-group-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <checkboxGroup id="verticalCheckboxGroup"
                       label="Vertical"
                       themeNames="vertical"
                       itemsEnum="io.jmix.uisamples.entity.CustomerGrade"/>
        <checkboxGroup id="horizontalCheckboxGroup"
                       label="Horizontal"
                       itemsEnum="io.jmix.uisamples.entity.CustomerGrade"/>
    </layout>
</view>




CheckboxGroupSimpleSample.java

package io.jmix.uisamples.view.flowui.components.checkboxgroup.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("checkbox-group-simple")
@ViewDescriptor("checkbox-group-simple.xml")
public class CheckboxGroupSimpleSample extends StandardView {
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


