<Path>Layouts > FormLayout > Simple FormLayout</Path>

formLayout is a responsive layout that arranges components into columns. The number of columns changes depending on the layout width. formLayout respects the nested components' properties. Use the colspan property to set the number of columns occupied by the component.

form-layout-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <tabSheet id="tabSheet" width="100%">
            <tab id="defaultTab" label="Default label position">
                <formLayout>
                    <textField label="TextField"/>
                    <dateTimePicker label="DateTimePicker"/>
                    <textArea label="TextArea"/>
                    <checkbox label="Checkbox"/>
                    <textArea label="TextArea with column span" colspan="2"/>
                    <passwordField label="PasswordField"/>
                    <emailField label="EmailField"/>
                </formLayout>
            </tab>
            <tab id="asideTab" label="Aside label position">
                <formLayout labelsPosition="ASIDE">
                    <formItem label="TextField">
                        <textField/>
                    </formItem>
                    <formItem label="DateTimePicker">
                        <dateTimePicker/>
                    </formItem>
                    <formItem label="TextArea">
                        <textArea/>
                    </formItem>
                    <formItem label="Checkbox">
                        <checkbox/>
                    </formItem>
                    <formItem label="TextArea with column span" colspan="2">
                        <textArea/>
                    </formItem>
                    <formItem label="PasswordField">
                        <passwordField/>
                    </formItem>
                    <formItem label="EmailField">
                        <emailField/>
                    </formItem>
                </formLayout>
            </tab>
        </tabSheet>
    </layout>
</view>




FormLayoutSimpleSample.java

package io.jmix.uisamples.view.flowui.containers.formlayout.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("form-layout-simple")
@ViewDescriptor("form-layout-simple.xml")
public class FormLayoutSimpleSample extends StandardView {
}


