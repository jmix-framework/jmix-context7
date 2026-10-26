<Path>Components > SVG</Path>

`Svg` renders SVG markup inline, as part of the page. The sample shows three ways to provide the markup:

- The nested `<content>` element. Wrap the markup in `CDATA`, otherwise the descriptor fails to load.
- The `file` attribute with a resource path loaded by `Resources`.
- The `setSvg()` method, which accepts a `String` or an `InputStream`. Use it for markup that is built in the controller.

Since the markup becomes part of the page, `currentColor` inside it resolves to the current text color, so the chart axis and the ring label follow the theme.

The component has no `width` and `height` attributes. Set the size in one of two ways:

- With the `width` and `height` attributes of the `<svg>` element in the markup itself, as in the "Content element" column.
- With the `css` attribute of the component or a CSS class added through `classNames`, as in the "File attribute" column. For the graphic to follow the component size, define only a `viewBox` in the markup, without `width` and `height`. The SVG then stretches to the component width, and its height follows the `viewBox` proportions.


svg.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout justifyContent="BETWEEN" classNames="horizontal-layout">
        <vbox padding="false" width="AUTO" alignItems="CENTER">
            <h4 text="Content element"/>
            <svg>
                <content><![CDATA[
                    <svg xmlns="http://www.w3.org/2000/svg" width="160" height="120" viewBox="0 0 160 120">
                        <circle cx="116" cy="36" r="18" fill="#ffb300"/>
                        <path d="M8 112 L58 44 L108 112 Z" fill="#66bb6a"/>
                        <path d="M64 112 L106 64 L152 112 Z" fill="#2e7d32"/>
                    </svg>
                ]]></content>
            </svg>
        </vbox>
        <vbox padding="false" width="AUTO" alignItems="CENTER">
            <h4 text="File attribute"/>
            <svg file="META-INF/resources/svg/bar-chart.svg" css="width: 160px"/>
        </vbox>
        <vbox padding="false" width="AUTO" alignItems="CENTER">
            <h4 text="setSvg() method"/>
            <svg id="progressSvg"/>
            <integerSlider id="progressSlider" width="10em" value="65" valueChangeMode="EAGER"/>
        </vbox>
    </layout>
</view>




SvgSample.java

package io.jmix.uisamples.view.flowui.components.svg;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.Svg;
import io.jmix.flowui.component.slider.JmixIntegerSlider;
import io.jmix.flowui.view.*;

import java.util.Locale;

@ViewController("svg")
@ViewDescriptor("svg.xml")
public class SvgSample extends StandardView {

    private static final String PROGRESS_SVG = """
            <svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="50" fill="none"
                        stroke="currentColor" stroke-opacity="0.15" stroke-width="12"/>
                <circle cx="60" cy="60" r="50" fill="none"
                        stroke="%s" stroke-width="12" pathLength="100" stroke-dasharray="%d 100"
                        transform="rotate(-90 60 60)"/>
                <text x="60" y="60" text-anchor="middle" dominant-baseline="central"
                      font-size="24" font-weight="600" fill="currentColor">%d%%</text>
            </svg>
            """;

    @ViewComponent
    private Svg progressSvg;
    @ViewComponent
    private JmixIntegerSlider progressSlider;

    @Subscribe
    public void onInit(InitEvent event) {
        updateProgress(progressSlider.getValue());
    }

    @Subscribe("progressSlider")
    public void onProgressSliderValueChange(ComponentValueChangeEvent<JmixIntegerSlider, Integer> event) {
        updateProgress(event.getValue());
    }

    private void updateProgress(int value) {
        progressSvg.setSvg(String.format(Locale.ROOT, PROGRESS_SVG, getProgressColor(value), value, value));
    }

    private String getProgressColor(int value) {
        if (value < 30) {
            return "#e53935";
        }

        return value < 70 ? "#fb8c00" : "#43a047";
    }
}




bar-chart.svg

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 120">
    <rect x="16" y="68" width="24" height="40" fill="#90caf9"/>
    <rect x="52" y="52" width="24" height="56" fill="#64b5f6"/>
    <rect x="88" y="36" width="24" height="72" fill="#42a5f5"/>
    <rect x="124" y="16" width="24" height="92" fill="#1e88e5"/>
    <path d="M8 108 H152" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
</svg>


