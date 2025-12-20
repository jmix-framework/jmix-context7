<Path>Components > CodeEditor > Simple CodeEditor</Path>

CodeEditor is a component to display and enter source code. It is multi-line text area featured with code highlighting and optional print margin and gutter with line numbers. UseSoftTabs property sets the tab character representing mode. Soft tabs mode means that tab character will be represented as a series of spaces. Hard tabs mode means that tab character will be represented as the special \t character. TextWrap property wraps text to the next line automatically. This way, horizontal scroll bars will not appear in the input field.

code-editor-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <hbox classNames="buttons-panel">
            <checkbox id="highlightCheckbox" label="Highlight active line" value="true"/>
            <checkbox id="highlightGutterCheckbox" label="Highlight gutter line" value="true"/>
            <checkbox id="gutterCheckbox" label="Show Gutter" value="true"/>
            <checkbox id="lineNumbersCheckbox" label="Line numbers" value="true"/>
            <checkbox id="printMarginCheckbox" label="Print margin" value="true"/>
            <checkbox id="useSoftTabsCheckbox" label="Use soft tabs" value="true"/>
            <checkbox id="textWrapCheckbox" label="Text wrap" value="false"/>
        </hbox>
        <codeEditor id="codeEditor"/>
    </layout>
</view>




CodeEditorSimpleSample.java

package io.jmix.uisamples.view.flowui.components.codeeditor.simple;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.component.codeeditor.CodeEditor;
import io.jmix.flowui.view.*;

@ViewController("code-editor-simple")
@ViewDescriptor("code-editor-simple.xml")
public class CodeEditorSimpleSample extends StandardView {

    @ViewComponent
    protected CodeEditor codeEditor;

    @Subscribe("highlightCheckbox")
    protected void onHighlightCheckboxValueChange(ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        codeEditor.setHighlightActiveLine(event.getValue());
    }

    @Subscribe("highlightGutterCheckbox")
    protected void onHighlightGutterCheckboxValueChange(ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        codeEditor.setHighlightGutterLine(event.getValue());
    }

    @Subscribe("gutterCheckbox")
    protected void onGutterCheckboxValueChange(ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        codeEditor.setShowGutter(event.getValue());
    }

    @Subscribe("lineNumbersCheckbox")
    protected void onLineNumbersCheckboxValueChange(ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        codeEditor.setShowLineNumbers(event.getValue());
    }

    @Subscribe("printMarginCheckbox")
    protected void onPrintMarginCheckboxValueChange(ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        codeEditor.setShowPrintMargin(event.getValue());
    }

    @Subscribe("useSoftTabsCheckbox")
    protected void onUseSoftTabsCheckboxValueChange(ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        codeEditor.setUseSoftTabs(event.getValue());
    }

    @Subscribe("textWrapCheckbox")
    protected void onTextWrapCheckboxValueChange(ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        codeEditor.setTextWrap(event.getValue());
    }
}


