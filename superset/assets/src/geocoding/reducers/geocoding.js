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
    return Object.assign({}, state, {
      columnList: action.columnList,
    });
  }
  if (action.type === actions.GET_COLUMNS_FOR_TABLE_FAILURE) {
    return Object.assign({}, state, {
      errorStatus: {
        message: action.message, timestamp: Date.now(),
      },
    });
  }
  if (action.type === actions.GEOCODE_PROGRESS_SUCCESS) {
    return Object.assign({}, state, {
      progress: action.progress,
    });
  }
  if (action.type === actions.GEOCODE_PROGRESS_FAILURE) {
    return Object.assign({}, state, {
      errorStatus: {
        message: action.message, timestamp: Date.now(),
      },
    });
  }
  if (action.type === actions.GEOCODE_SUCCESS) {
    return Object.assign({}, state, {
      infoStatus: {
        message: 'Geocoding successfully ended.', timestamp: Date.now(),
      },
    });
  }
  if (action.type === actions.GEOCODE_FAILURE) {
    return Object.assign({}, state, {
      errorStatus: {
        message: action.message, timestamp: Date.now(),
      },
    });
  }
  if (action.type === actions.GEOCODE_INTERRUPT_SUCCESS) {
    return Object.assign({}, state, {
      infoStatus: {
        message: 'Geocoding successfully interrupted.', timestamp: Date.now(),
      },
    });
  }
  if (action.type === actions.GEOCODE_INTERRUPT_FAILURE) {
    return Object.assign({}, state, {
      errorStatus: {
        message: action.message, timestamp: Date.now(),
      },
    });
  }

  return state;
}