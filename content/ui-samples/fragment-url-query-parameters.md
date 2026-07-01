<Path>Fragments > Fragments facets > UrlQueryParameters</Path>

`urlQueryParameters` facet is designed for declarative binding of the fragment state to the URL. It allows
you to
preserve the fragment state when navigating between views or refreshing the browser page.

The obvious example is the entity list view with fragment with `dataGrid`, pagination and filtering. You will want to
preserve pagination and filtering parameters when refreshing the browser page and when navigating to a detail view and
back.

Supported components:

- `pagination`
- `propertyFilter`
- `genericFilter`
- `dataGridHeaderFilter`

In this sample, when opening the view, the age filter condition was automatically applied from the URL. You can use
pagination and see that new parameters have been added to the URL. After reloading the page, the state of these
components will be restored.


fragment-url-query-parameters.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <fragment id="fragment"
                  class="io.jmix.uisamples.view.flowui.fragments.facets.urlqueryparameters.UrlQueryParametersFragment"/>
    </layout>
</view>




FragmentUrlQueryParametersSample.java

package io.jmix.uisamples.view.flowui.fragments.facets.urlqueryparameters;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("fragment-url-query-parameters")
@ViewDescriptor("fragment-url-query-parameters.xml")
public class FragmentUrlQueryParametersSample extends StandardView {
}




url-query-parameters-fragment.xml

<fragment xmlns="http://jmix.io/schema/flowui/fragment">
    <data readOnly="true">
        <collection id="customersDc"
                    class="io.jmix.uisamples.entity.Customer"
                    fetchPlan="_local">
            <loader id="customersDl">
                <query>
                    <![CDATA[select e from Customer e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <urlQueryParameters>
            <genericFilter component="genericFilter"/>
            <pagination component="pagination"/>
        </urlQueryParameters>
        <fragmentDataLoadCoordinator auto="true"/>
    </facets>
    <content>
        <vbox padding="false">
            <genericFilter id="genericFilter" dataLoader="customersDl">
                <properties include=".*"/>
            </genericFilter>
            <hbox id="buttonsPanel" width="100%" wrap="true">
                <simplePagination id="pagination" dataLoader="customersDl" itemsPerPageItems="5"/>
            </hbox>
            <dataGrid id="customersDataGrid"
                      width="100%"
                      minHeight="15em"
                      dataContainer="customersDc">
                <columns>
                    <column property="name"/>
                    <column property="lastName"/>
                    <column property="email"/>
                    <column property="age"/>
                    <column property="active"/>
                    <column property="grade"/>
                </columns>
            </dataGrid>
        </vbox>
    </content>
</fragment>




UrlQueryParametersFragment.java

package io.jmix.uisamples.view.flowui.fragments.facets.urlqueryparameters;

import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.flowui.fragment.Fragment;
import io.jmix.flowui.fragment.FragmentDescriptor;

@FragmentDescriptor("url-query-parameters-fragment.xml")
public class UrlQueryParametersFragment extends Fragment<VerticalLayout> {
}


