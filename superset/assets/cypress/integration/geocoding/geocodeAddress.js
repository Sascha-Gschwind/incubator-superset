/** Licensed to the Apache Software Foundation (ASF) under one
* or more contributor license agreements.  See the NOTICE file
* distributed with this work for additional information
* regarding copyright ownership.  The ASF licenses this file
* to you under the Apache License, Version 2.0 (the
* "License"); you may not use this file except in compliance
* with the License.  You may obtain a copy of the License at
*
*   http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing,
* software distributed under the License is distributed on an
* "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
* KIND, either express or implied.  See the License for the
* specific language governing permissions and limitations
* under the License.
 */

export default () => {
    // before


    // after

    describe('geocode data from a table', () => {
      /*   before (function() {
              cy.login();
            cy.server();
         cy.visit('/databaseview/edit/1');
        cy.get('#allow_dml').check(true);

        cy.get('button').contains('Save').click();
    }); */
        beforeEach(() => {
             cy.login();
            cy.server();
         cy.visit('/databaseview/edit/1');
         cy.url({ timeout: 3000 }).should('include', '/databaseview/edit/');
         cy.get('#force_ctas_schema');
            cy.get('#allow_dml').then((elem) => {
            elem.val(true);
            });

            cy.get('button').contains('Save').click();
            //cy.url({ timeout: 3000 }).should('include', '/databaseview/list');
            cy.visit('/geocoder/geocoding')
            //    cy.route('/tabelmodelview/list').as('finish_geocoding');
        });

        it('test geocoding of simple data', () => {
            cy.url({timeout:3000}).should('include', 'geocoder/geocoding');
            cy.url({timeout:3000}).should('not.include', 'databaseview');
            cy.contains('Geocode');
            cy.get('#alert-danger').should('not.exist');
            cy.get('button').contains('Geocode').click();
            cy.contains("need to select");
            cy.get('#datasource').then((elem) => {
                elem.val('0');
            });
            cy.get('button').contains('Geocode').click();
            cy.contains("At least one column needs");
            cy.log ("contained at least one column needed");
            cy.wait(500);
            // problem here probably since it's disabled until we select a datasource
            cy.get('#countryColumn').then((elem) => {
                elem.val('country_name');
            });
            cy.log("found countryColumn");

            cy.get('#geocoder').then((elem) => {
                elem.val('testing_geocoder');
            });
            cy.log("set geocoder");
             cy.get('button').contains('Geocode').click();
            cy.url({ timeout: 30000 }).should('include', '/tablemodelview/list');
        });

        it ('test 2', () => {
             cy.url({timeout:3000}).should('include', 'geocoder/geocoding');
            cy.get('#alert-danger').should('not.exist');
             cy.get('#datasource').then((elem) => {
                 elem.val('0');
             });
              cy.get('button').contains('Geocode').click();
              if(cy.contains("You need to select a datasource")) {
                  cy.get('#datasource').val == 0;
              }
            cy.contains("At least one column needs");
                 cy.get('#countryColumn').then((elem) => {
                     elem.val('country_name');
                 });
                 cy.get('button').contains('Geocode').click();
            cy.url({ timeout: 30000 }).should('include', '/tablemodelview/list');
            });


        it ("test3", () => {
              cy.url({timeout:3000}).should('include', 'geocoder/geocoding');
            cy.get('#alert-danger').should('not.exist');
            cy.get('#datasource').then((elem) => {
                        elem.val('0');
                    });
                    cy.get('button').contains('Geocode').click();
                    cy.contains("At least one column needs");
                    cy.log ("contained at least one column needed");
                    cy.wait(500);
                    // problem here probably since it's disabled until we select a datasource
                    cy.get('#countryColumn').then((elem) => {
                        elem.val('country_name');
                    });
                    cy.log("found countryColumn");

                    cy.get('#geocoder').then((elem) => {
                        elem.val('0');
                    });
                    cy.log("set geocoder");
                     cy.get('button').contains('Geocode').click();
                    cy.url({ timeout: 30000 }).should('include', '/tablemodelview/list');
        });
        after (function() {
        cy.visit('/databaseview/edit/1');
        cy.get('#allow_dml').uncheck();
        cy.get('button').contains('Save').click();
    });
    });
};
