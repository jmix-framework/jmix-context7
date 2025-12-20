<Path>Cookbook > Other recipes > Displaying PDF in an IFrame using REST</Path>

This sample demonstrates possible approaches for displaying PDF files from the file storage using the IFrame component and REST API. This method is convenient if the document is stored in an entity as a FileRef. If your application is configured with a Generic REST API you can simply specify the request address as the source for the IFrame (see Files API :: Jmix Documentation). Thus, this request will receive a file that will be displayed using standard browser tools in IFrame. In this example, a custom request controller was configured. See CustomFileDownloadController.java. In order for this type of requests to be processed correctly by the application, it is required to add a special security filter. See CustomRestSecurityConfiguration.java. This source code contains a directive that allows the use of resources if the requests is sent from demo.jmix.io. More detailed information is available in the documentation for the directive: CSP: frame-ancestors - HTTP | MDN 6.

iframe-pdf-rest.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <iframe id="fileRefIframe" width="100%" height="100%" css="border: unset;"/>
    </layout>
</view>




IframePdfRestSample.java

package io.jmix.uisamples.view.flowui.cookbook.iframepdfrest;

import com.vaadin.flow.component.UI;
import com.vaadin.flow.component.html.IFrame;
import com.vaadin.flow.component.page.Page;
import io.jmix.core.FileRef;
import io.jmix.core.common.util.URLEncodeUtils;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.bean.SamplesFileStorage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.web.context.WebApplicationContext;

@ViewController("iframe-pdf-rest")
@ViewDescriptor("iframe-pdf-rest.xml")
public class IframePdfRestSample extends StandardView {

    private static final String REST_PATH = "/custom-rest/files?fileRef=";
    private static final FileRef FILE_REF = FileRef.create(
            SamplesFileStorage.DEFAULT_STORAGE_NAME,
            "documentation.pdf",
            "documentation.pdf"
    );

    @Autowired
    private ApplicationContext applicationContext;
    @ViewComponent
    private IFrame fileRefIframe;

    @Subscribe
    public void onInit(InitEvent event) {
        Page page = UI.getCurrent().getPage();

        page.fetchCurrentURL(url -> {
            String contextPath = ((WebApplicationContext) applicationContext).getServletContext().getContextPath();

            String documentSrc = url.getProtocol() + "://" + url.getAuthority() + contextPath +
                    REST_PATH + URLEncodeUtils.encodeUtf8(FILE_REF.toString());

             fileRefIframe.setSrc(documentSrc);
        });
    }
}




CustomRestSecurityConfiguration.java

package io.jmix.uisamples.view.flowui.cookbook.iframepdfrest;

import io.jmix.core.JmixSecurityFilterChainOrder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class CustomRestSecurityConfiguration {

    @Bean
    @Order(JmixSecurityFilterChainOrder.FLOWUI - 10)
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http.securityMatcher("/custom-rest/files/**")
                .authorizeHttpRequests((authorize) -> authorize.requestMatchers("/custom-rest/files/**").permitAll());
        http.headers(headers ->
                headers.contentSecurityPolicy(secPolicy ->
                        secPolicy.policyDirectives("frame-ancestors demo.jmix.io")
                )
        );

        return http.build();
    }
}




CustomFileDownloadController.java

package io.jmix.uisamples.rest;

import io.jmix.core.FileRef;
import io.jmix.core.FileTransferService;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController("uisamples_CustomFileDownloadController")
@RequestMapping("/custom-rest")
public class CustomFileDownloadController {

    protected FileTransferService fileTransferService;

    public CustomFileDownloadController(FileTransferService fileTransferService) {
        this.fileTransferService = fileTransferService;
    }

    @GetMapping(path = "/files")
    public void getFileRef(@RequestParam String fileRef,
                           HttpServletResponse response) {
        try {
            FileRef fileReference = FileRef.fromString(fileRef);
            String storageName = fileReference.getStorageName();
            fileTransferService.downloadAndWriteResponse(fileReference, storageName, false, response);
        } catch (IllegalArgumentException e) {
            throw new RuntimeException("Invalid file reference", e);
        }
    }
}


