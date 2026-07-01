<Path>Components > Select > Simple Select</Path>

A Select is a lighter component than a ComboBox. Use select when you don't need user input and items filtering.

select-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <select itemsEnum="io.jmix.uisamples.entity.CustomerGrade"
                emptySelectionAllowed="true" emptySelectionCaption="Empty"/>
    </layout>
</view>




SelectSimpleSample.java

package io.jmix.uisamples.view.flowui.components.select.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("select-simple")
@ViewDescriptor("select-simple.xml")
public class SelectSimpleSample extends StandardView {
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


