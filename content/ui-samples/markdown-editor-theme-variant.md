<Path>Components > Markdown Components > MarkdownEditor with ThemeVariant</Path>

The `MarkdownEditor` component supports the following theme variants:

- `toolbar-align-start` — aligns the toolbar buttons to the start side of the header.
- `toolbar-align-center` — centers the toolbar buttons and hides the divider.
- `toolbar-align-end` — aligns the toolbar buttons to the end side of the header and hides the divider.
- `helper-above-field` — renders the helper text above the field, below the label.

You can apply these variants using the `themeNames` attribute in the XML descriptor or in the view controller using
constants from the `MarkdownEditorVariant` class.


markdown-editor-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <details summaryText="Toolbar align variant" opened="true">
            <hbox wrap="true">
                <markdownEditor label="Align start" themeNames="toolbar-align-start"
                                placeholder="Placeholder"/>
                <markdownEditor label="Align center" themeNames="toolbar-align-center"
                                placeholder="Placeholder"/>
                <markdownEditor label="Align end" themeNames="toolbar-align-end"
                                placeholder="Placeholder"/>
            </hbox>
        </details>
        <details summaryText="Helper variant" opened="true">
            <hbox wrap="true">
                <markdownEditor label="Default helper" helperText="Default helper text"/>
                <markdownEditor label="Helper above field" themeNames="helper-above-field"
                                helperText="Above helper text"/>
            </hbox>
        </details>
    </layout>
</view>




MarkdownEditorThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.markdowncomponents.markdowneditorthemevariant;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("markdown-editor-theme-variant")
@ViewDescriptor("markdown-editor-theme-variant.xml")
public class MarkdownEditorThemeVariantSample extends StandardView {
}


