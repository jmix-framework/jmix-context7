<Path>Cookbook > Other recipes > Displaying a dynamic PDF in an IFrame</Path>

This sample demonstrates possible approaches for displaying PDF files as a dynamic resource using the `IFrame`
component.

To make displaying such resources available, you need to configure the `frame-ancestors` policy directive. See [
`IframeCustomSecurity.java`]({currentPath}?tab=IframeCustomSecurity.java).

Dynamic resources are loaded on the client-side using the `DownloadHandler` objects.

`DownloadHandler` provides generated URI. Registration of the resource URI is automatically handled by
components that explicitly support stream resources (including `IFrame`).\
This way, the resource will be cleaned up when the component is removed from the view.

This source code contains a directive that allows the use of resources if the requests is sent from `demo.jmix.io`.\
More detailed information is available in the documentation for the
directive: [CSP: frame-ancestors - HTTP | MDN 6](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors).


iframe-pdf-dynamic.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <button id="newResourceBtn" text="msg://newResourceBtn.text" icon="FILE_REFRESH"
                disableOnClick="true"/>
        <iframe id="iframe" width="100%" height="100%" css="border: unset;"/>
    </layout>
</view>




IframePdfDynamicSample.java

package io.jmix.uisamples.view.flowui.cookbook.iframepdfdynamic;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.html.IFrame;
import com.vaadin.flow.server.streams.DownloadHandler;
import io.jmix.core.Resources;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("iframe-pdf-dynamic")
@ViewDescriptor("iframe-pdf-dynamic.xml")
public class IframePdfDynamicSample extends StandardView {

    private static final String PDF_BASE_PACKAGE = "/META-INF/resources/pdf";
    private static final String TUTORIAL_PDF_PATH = PDF_BASE_PACKAGE + "/tutorial.pdf";
    private static final String DOCUMENTATION_PDF_PATH = PDF_BASE_PACKAGE + "/documentation.pdf";

    @ViewComponent
    private IFrame iframe;

    @Autowired
    private Resources resources;

    @Subscribe
    public void onInit(InitEvent event) {
        // any other file can be provided in this way
        iframe.setSrc(DownloadHandler.forClassResource(getClass(), TUTORIAL_PDF_PATH));
    }

    @Subscribe("newResourceBtn")
    public void onNewResourceBtnClick(ClickEvent<JmixButton> event) {
        iframe.setSrc(DownloadHandler.forClassResource(getClass(), DOCUMENTATION_PDF_PATH));
    }
}




IframeCustomSecurity.java

package io.jmix.uisamples.view.flowui.cookbook.iframepdf;

import io.jmix.securityflowui.security.FlowuiVaadinWebSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;

@EnableWebSecurity
public class IframeCustomSecurity extends FlowuiVaadinWebSecurity {

    @Override
    public void configure(HttpSecurity http) throws Exception {
        super.configure(http);

        http.headers(headers ->
                headers.contentSecurityPolicy(
                        secPolicy -> secPolicy.policyDirectives("frame-ancestors demo.jmix.io")
                )
        );
    }
}


