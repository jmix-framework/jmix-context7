<Path>Components > ValuePicker > MultiValuePicker with enums</Path>

Use the enumClass action property to set the enumeration class used as the type of selected value.

value-picker-multi-enum.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="flex-row">
        <multiValuePicker id="multiValuePicker">
            <actions>
                <action id="select" type="multi_value_select">
                    <properties>
                        <property name="enumClass" value="io.jmix.uisamples.entity.CustomerGrade"/>
                    </properties>
                </action>
                <action id="clear" type="value_clear"/>
            </actions>
        </multiValuePicker>
    </layout>
</view>




ValuePickerMultiEnumSample.java

package io.jmix.uisamples.view.flowui.components.valuepicker.multienum;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("value-picker-multi-enum")
@ViewDescriptor("value-picker-multi-enum.xml")
public class ValuePickerMultiEnumSample extends StandardView {
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


