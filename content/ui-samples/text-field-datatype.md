<Path>Components > TextField > TextField with Datatype</Path>

If the field is not connected to an entity attribute (i.e. the dataContainer and property are not set), you can set the field value type in the datatype attribute. The attribute value accepts any data type registered in the application metadata - see Datatype. Typically, TextField uses the following data types: decimal int double

text-field-datatype.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="horizontal-layout">
        <textField id="stringTextField" label="String"
                   datatype="string"/>
        <textField id="integerTextField" label="Integer"
                   datatype="int"/>
        <textField id="doubleTextField" label="Double"
                   datatype="double"/>
    </layout>
</view>




TextFieldDatatypeSample.java

package io.jmix.uisamples.view.flowui.components.textfield.datatype;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("text-field-datatype")
@ViewDescriptor("text-field-datatype.xml")
public class TextFieldDatatypeSample extends StandardView {
}


