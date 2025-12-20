<Path>Cookbook > Other recipes > Displaying a static PDF in an IFrame</Path>

This sample demonstrates possible approaches for displaying PDF files as a static resource using the IFrame component. Static resources should be stored in the META-INF/resources folder. To make displaying such resources available, you need to configure the frame-ancestors policy directive. See IframeCustomSecurity.java. This source code contains a directive that allows the use of resources if the requests is sent from demo.jmix.io. More detailed information is available in the documentation for the directive: CSP: frame-ancestors - HTTP | MDN 6.

iframe-pdf.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <iframe width="100%" height="100%" css="border: unset;"
                resource="pdf/tutorial.pdf"/>
    </layout>
</view>




IframePdfSample.java

package io.jmix.uisamples.view.flowui.cookbook.iframepdf;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("iframe-pdf")
@ViewDescriptor("iframe-pdf.xml")
public class IframePdfSample extends StandardView {
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


