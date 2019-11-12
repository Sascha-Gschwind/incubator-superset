/**
 * Licensed to the Apache Software Foundation (ASF) under one
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
import * as actions from '../actions/geocoding';

export default function geocodingReducer(state = {}, action) {
  if (action.type === actions.GET_COLUMNS_FOR_TABLE_SUCCESS) {
    // TODO: Save columns to store
  }
  if (action.type === actions.GET_COLUMNS_FOR_TABLE_FAILURE) {
    // TODO: Save error message to store
  }
  if (action.type === actions.GEOCODE_PROGRESS_SUCCESS) {
    // TODO: Save progress in store
  }
  if (action.type === actions.GEOCODE_PROGRESS_FAILURE) {
    // TODO: Save error message to store
  }
  if (action.type === actions.GEOCODE_SUCCESS) {
    // TODO: What to do now?
  }
  if (action.type === actions.GEOCODE_FAILURE) {
    // TODO: Save error message in store
  }
  if (action.type === actions.GEOCODE_INTERRUPT_SUCCESS) {
    // TODO: What to do now?
  }
  if (action.type === actions.GEOCODE_INTERRUPT_FAILURE) {
    // TODO: Save error message in store
  }

  return state;
}
