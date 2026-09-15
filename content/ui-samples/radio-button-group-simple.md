<Path>Components > RadioButtonGroup > Simple RadioButtonGroup</Path>

RadioButtonGroup allows a user to select signle value from a list of options using radio-buttons. The themeNames attribute defines the orientation of group elements. By default, elements are arranged horizontally. In this example, RadioButtonGroup is used to select an enumeration value for an entity attribute.

radio-button-group-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <radioButtonGroup id="verticalRadioButtonGroup"
                       label="Vertical"
                       themeNames="vertical"
                       itemsEnum="io.jmix.uisamples.entity.CustomerGrade"/>
        <radioButtonGroup id="horizontalRadioButtonGroup"
                       label="Horizontal"
                       themeNames="horizontal"
                       itemsEnum="io.jmix.uisamples.entity.CustomerGrade"/>
    </layout>
</view>




RadioButtonGroupSimpleSample.java

package io.jmix.uisamples.view.flowui.components.radiobuttongroup.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("radio-button-group-simple")
@ViewDescriptor("radio-button-group-simple.xml")
public class RadioButtonGroupSimpleSample extends StandardView {
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


